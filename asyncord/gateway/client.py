"""Websocket gateway client for the Discord API.

References:
https://discord.com/developers/docs/topics/gateway
"""

from __future__ import annotations

import asyncio
import logging
from math import floor
from typing import Any, TypeVar, cast

import aiohttp
from aiohttp import ClientWebSocketResponse, WSMsgType
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
from asyncord.gateway.hearbeat import Heartbeat
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


class GatewayClient:
    """Class for the gateway client.

    Attributes:
        token (str): Token to use for authentication.
        intents (Intent): Intents to use for the client.
        dispatcher (EventDispatcher): Event dispatcher.
        is_started (bool): Whether the client is started.
    """

    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession,
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
        self.is_started = False

        self._ws_url = ws_url
        self._resume_url = None

        self._session_id = None
        self._last_seq_number = 0
        self._session = session
        self._heartbeat = Heartbeat(self.heartbeat, self._handle_heartbeat_timeout)

    async def start(self) -> None:
        """Start the gateway client."""
        self.is_started = True

        async with self._session.ws_connect(self.url) as ws:
            self.ws = ws
            logger.info('Connected to gateway')

            for _ in range(5, 0, -1):
                try:
                    await self._ws_loop(ws)
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
                raise RuntimeError('Could not connect to the gateway')

    async def stop(self) -> None:
        """Stop the gateway client."""
        await self._heartbeat.stop()
        self.is_started = False
        if self.ws:
            await self.ws.close()

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
        payload = command_data.model_dump(mode='json', exclude_none=True)
        await self._send_command(GatewayCommandOpcode.IDENTIFY, payload)

    async def heartbeat(self) -> None:
        """Send a heartbeat to the gateway."""
        await self._send_command(GatewayCommandOpcode.HEARTBEAT, None)

    async def resume(self, command_data: ResumeCommand) -> None:
        """Resume a previous session.

        Args:
            command_data(ResumeCommand): Data to send to the gateway.
        """
        await self._send_command(GatewayCommandOpcode.RESUME, command_data.model_dump(mode='json'))

    async def update_presence(self, presence_data: PresenceUpdateData) -> None:
        """Update the client's presence.

        Args:
            presence_data (PresenceUpdateData): Data to send to the gateway.
        """
        prepared_data = presence_data.model_dump(mode='json')
        await self._send_command(GatewayCommandOpcode.PRESENCE_UPDATE, prepared_data)

    @property
    def url(self) -> StrOrURL:
        """Return the URL of the websocket connection.

        Returns:
            StrOrURL: The URL of the websocket connection.
        """
        return self._resume_url or self._ws_url

    async def _ws_loop(self, ws: ClientWebSocketResponse) -> None:
        while self.is_started:
            msg = await ws.receive()

            if msg.type == WSMsgType.TEXT:
                await self._handle_message(GatewayMessage(**msg.json()))

            elif msg.type in {WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED}:
                logger.info(f'Connection closed: {msg.data} {msg.extra}')
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
                        self._resume_url = event.resume_gateway_url
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
                await self._heartbeat.ack()

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
        heartbeat_period = floor(event.heartbeat_interval / 1000)
        await self._heartbeat.reset_heartbeat(heartbeat_period)
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
        self._resume_url = event.resume_gateway_url

    async def _handle_heartbeat_timeout(self) -> None:
        """Handle a heartbeat timeout."""
        await self.stop()


async def main() -> None:
    """Main function for fast gateway testing."""
    session = aiohttp.ClientSession()
    c = GatewayClient('OTM0NTY0MjI1NzY5MTQ4NDM2.Yex6wg.AAkUaqRS0ACw8__ERfQ6d8gOdkE', session=session)

    async def test_ready_handler(_: ReadyEvent, gateway: GatewayClient) -> None:  # noqa: PT019
        await gateway.update_presence(PresenceUpdateData(
            activities=[
                Activity(
                    name='with you',
                    type=ActivityType.GAME,
                ),
            ],
        ))
    c.add_handler(test_ready_handler)

    async def test_get_message_handler(event: MessageCreateEvent, gateway: GatewayClient) -> None:
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
    await session.close()


if __name__ == '__main__':
    asyncio.run(main())
