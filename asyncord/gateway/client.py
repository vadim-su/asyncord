from __future__ import annotations

import asyncio
import logging
import random
from math import floor
from typing import Any, TypeVar, cast

import aiohttp
from aiohttp import WSMsgType
from loguru import logger
from rich.logging import RichHandler
from rich.pretty import pretty_repr

from asyncord.client.models.activity import Activity, ActivityType
from asyncord.gateway import errors
from asyncord.gateway.commands import IdentifyCommand, PresenceUpdateData, ResumeCommand
from asyncord.gateway.dispatcher import EventDispatcher, EventHandlerType
from asyncord.gateway.events.base import GatewayEvent, HelloEvent, ReadyEvent
from asyncord.gateway.events.event_map import EVENT_MAP
from asyncord.gateway.events.messages import MessageCreateEvent
from asyncord.gateway.intents import DEFAULT_INTENTS, Intent
from asyncord.gateway.message import GatewayCommandOpcode, GatewayEventOpcode, GatewayMessage
from asyncord.typedefs import StrOrURL
from asyncord.urls import GATEWAY_URL

logger.configure(handlers=[{
    'sink': RichHandler(
        omit_repeated_times=False,
        rich_tracebacks=True,
    ),
    'format': '{message}',
}])


_EVENT_T = TypeVar('_EVENT_T', bound=GatewayEvent)


class AsyncGatewayClient:
    """A client for the Discord Gateway API."""

    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession | None = None,
        intents: Intent = DEFAULT_INTENTS,
        ws_url: StrOrURL = GATEWAY_URL,
    ):
        """Initialize client.

        Args:
            token (str): Token to use for authentication.
            session (aiohttp.ClientSession, None): Session to use for requests.
            intents (Intent): Intents to use for the client.
            ws_url (StrOrURL): URL to connect to. Defaults to the Discord Gateway URL.
        """
        self.token = token
        self.intents = intents
        self.dispatcher = EventDispatcher()
        self.dispatcher.add_argument('gateway', self)
        self.ws = None

        self.ws_url = ws_url
        self.resume_url = None

        self._session_id = None
        self._last_seq_number = 0
        self._session: aiohttp.ClientSession | None = session
        self._check_heartbeat_ack_task = None
        self._heartbeat_task = None

    def add_handler(self, event_handler: EventHandlerType[_EVENT_T, ...]) -> None:
        """Add an event handler.

        Args:
            event_handler (EventHandlerType[_EVENT_T]): The event handler to add.
        """
        self.dispatcher.add_handler(event_handler)

    async def identify(self, command_data: IdentifyCommand) -> None:
        """Identify with the gateway.

        Args:
            command_data (IdentifyCommand): The data to send to the gateway.
        """
        payload = command_data.dict(exclude_none=True)
        await self._send_command(GatewayCommandOpcode.IDENTIFY, payload)

    async def heartbeat(self) -> None:
        """Send a heartbeat to the gateway."""
        await self._send_command(GatewayCommandOpcode.HEARTBEAT, None)

    async def resume(self, command_data: ResumeCommand) -> None:
        """Resume a previous session.

        Args:
            command_data(ResumeCommand): Data to send to the gateway.
        """
        await self._send_command(GatewayCommandOpcode.RESUME, command_data.dict())

    async def update_presence(self, presence_data: PresenceUpdateData) -> None:
        """Update the client's presence.

        Args:
            presence_data (PresenceUpdateData): Data to send to the gateway.
        """
        prepared_data = presence_data.model_dump(mode='json')
        await self._send_command(GatewayCommandOpcode.PRESENCE_UPDATE, prepared_data)

    async def start(self) -> None:
        """Start the gateway client."""
        if self._session:
            session = self._session
        else:
            session = aiohttp.ClientSession()

        for _ in range(5, 0, -1):
            try:
                await self._ws_loop(session)
                break

            except (
                aiohttp.ClientConnectorError,
                errors.HeartbeatAckTimeoutError,
                errors.InvalidSessionError,
            ) as err:
                logging.error(err)
                await asyncio.sleep(5)

            except errors.NecessaryReconnectError:
                logging.info('Reconnect is necessary')

        else:
            if not self._session:
                await session.close()
            raise RuntimeError('Could not connect to the gateway')

        if not self._session:
            await session.close()

    @property
    def url(self) -> StrOrURL:
        """Return the URL of the websocket connection.

        Returns:
            StrOrURL: The URL of the websocket connection.
        """
        return self.resume_url or self.ws_url

    async def _ws_loop(self, session: aiohttp.ClientSession) -> None:
        async with session.ws_connect(self.url) as ws:
            self.ws = ws
            logger.info('Connected to gateway')

            while True:
                msg = await ws.receive()

                if msg.type == WSMsgType.TEXT:
                    await self._handle_message(GatewayMessage(**msg.json()))

                elif msg.type in {WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED}:
                    logger.info(f'Connection closed: {msg.data} {msg.extra}')
                    if self._check_heartbeat_ack_task:
                        await self._check_heartbeat_ack_task
                    break

                else:
                    logger.warning(f'Unhandled websocket message type: {msg.type}')

    async def _send_command(self, op: GatewayCommandOpcode, command_data: Any) -> None:  # noqa: ANN401
        """Send a command to the gateway.

        Args:
            op (GatewayCommandOpcode): Opcode of the command.
            command_data (Any): Command data to send.

        Raises:
            RuntimeError: If the client is not connected.
        """
        if not self.ws:
            raise RuntimeError('Client is not connected')
        await self.ws.send_json({'op': op, 'd': command_data})

    async def _handle_message(self, msg: GatewayMessage) -> None:
        """Handle a message from the gateway.

        This method is responsible for dispatching events to the registered handlers.

        Args:
            msg (GatewayMessage): The message to handle.

        Raises:
            InvalidSessionError: If the session is invalid.
        """
        logger.debug('Got message:\n{0}', pretty_repr(msg))
        self._last_seq_number = max(self._last_seq_number, msg.sequence_number or 0)

        match msg.opcode:
            case GatewayEventOpcode.DISPATCH:
                event_class = EVENT_MAP.get(cast(str, msg.event_name))
                if event_class:
                    event = event_class.model_validate(msg.msg_data)
                    if isinstance(event, ReadyEvent):
                        self.resume_url = event.resume_gateway_url
                        self._session_id = event.session_id

                    await self.dispatcher.dispatch(event)
                else:
                    logger.warning("Event '{0}' unhandled", msg.event_name)

            case GatewayEventOpcode.INVALID_SESSION:
                session_id = cast(str, self._session_id)
                self._session_id = None
                self._last_seq_number = 0
                raise errors.InvalidSessionError(session_id)

            case GatewayEventOpcode.HELLO:
                event = HelloEvent.model_validate(msg.msg_data)
                await self._hello(event)

            case GatewayEventOpcode.HEARTBEAT_ACK:
                await self._heartbeat_ack()

            case GatewayEventOpcode.RECONNECT:
                self._session_id = None
                self._last_seq_number = 0
                raise errors.NecessaryReconnectError

            case _:
                logger.warning('Unhandled message:\n{0}', pretty_repr(msg))

    async def _hello(self, event: HelloEvent) -> None:
        """Handle a hello event.

        Args:
            event (HelloEvent): The event to handle.
        """
        await self._reset_heartbeat(floor(event.heartbeat_interval / 1000))
        if self._session_id:
            await self.resume(ResumeCommand(
                token=self.token,
                session_id=self._session_id,
                seq=self._last_seq_number,
            ))
        else:
            await self.identify(IdentifyCommand(token=self.token, intents=self.intents))

    async def _ready(self, event: ReadyEvent) -> None:
        """Handle the ready event."""
        self.resume_url = event.resume_gateway_url

    async def _heartbeat_ack(self) -> None:
        """Handle a heartbeat ack."""
        if self._check_heartbeat_ack_task:
            self._check_heartbeat_ack_task.cancel()

    async def _heartbeat_loop(self, heartbeat_period: float) -> None:
        """Start the heartbeat loop.

        Args:
            heartbeat_period (float): The period of the heartbeat in seconds.
        """
        while True:
            await self.heartbeat()
            if self._check_heartbeat_ack_task:
                self._check_heartbeat_ack_task.cancel()
            next_run = max(heartbeat_period * random.random(), heartbeat_period / 4, 10)  # noqa: S311
            next_run = round(next_run, 3)
            logger.debug('Heartbeat sent. Next run in {0} seconds', next_run)

            self._check_heartbeat_ack_task = asyncio.create_task(
                self._wait_heartbeat_ack(next_run / 2),
            )
            await asyncio.sleep(next_run)

    async def _wait_heartbeat_ack(self, wait_for: float) -> None:
        """Check if the last heartbeat was acknowledged.

        Args:
            wait_for (float): The time to wait for the ack.
        """
        await asyncio.sleep(wait_for)
        logger.warning('Heartbeat ack timeout')
        if self.ws:
            await self.ws.close()

        raise errors.HeartbeatAckTimeoutError(wait_for)

    async def _reset_heartbeat(self, heartbeat_period: float) -> None:
        """Reset the heartbeat loop.

        Args:
            heartbeat_period (float): The period of the heartbeat in seconds.
        """
        if self._check_heartbeat_ack_task:
            self._check_heartbeat_ack_task.cancel()
            self._check_heartbeat_ack_task = None

        if self._heartbeat_task:
            self._heartbeat_task.cancel()

        self._heartbeat_task = asyncio.create_task(
            self._heartbeat_loop(heartbeat_period),
        )


async def main():
    c = AsyncGatewayClient('OTM0NTY0MjI1NzY5MTQ4NDM2.Yex6wg.AAkUaqRS0ACw8__ERfQ6d8gOdkE')

    async def test_ready_handler(_: ReadyEvent, gateway: AsyncGatewayClient) -> None:
        await gateway.update_presence(PresenceUpdateData(
            activities=[
                Activity(
                    name='with you',
                    type=ActivityType.GAME,
                ),
            ],
        ))
    c.add_handler(test_ready_handler)

    async def test_get_message_handler(event: MessageCreateEvent, gateway: AsyncGatewayClient) -> None:
        await gateway.update_presence(PresenceUpdateData(
            activities=[
                Activity(
                    name=event.content,
                    type=ActivityType.GAME,
                ),
            ],
        ))

    c.add_handler(test_get_message_handler)

    await c.start()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
