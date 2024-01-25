"""Websocket gateway client for the Discord API.

References:
https://discord.com/developers/docs/topics/gateway
"""

from __future__ import annotations

import asyncio
import logging
from math import floor
from typing import Any, Sequence, cast

import aiohttp
from aiohttp import ClientWebSocketResponse, WSMsgType
from pydantic import ValidationError
from rich.pretty import pretty_repr

from asyncord.gateway import errors
from asyncord.gateway.commands import IdentifyCommand, PresenceUpdateData, ResumeCommand
from asyncord.gateway.dispatcher import EventDispatcher, EventHandlerType
from asyncord.gateway.events.base import GatewayEvent, HelloEvent, ReadyEvent
from asyncord.gateway.events.event_map import EVENT_MAP
from asyncord.gateway.hearbeat import Heartbeat
from asyncord.gateway.intents import DEFAULT_INTENTS, Intent
from asyncord.gateway.messages.message import GatewayCommandOpcode, GatewayMessageAdapter, GatewayMessageOpcode
from asyncord.typedefs import StrOrURL
from asyncord.urls import GATEWAY_URL

logger = logging.getLogger(__name__)


class GatewayClient:
    """Class for the gateway client.

    Attributes:
        token: Token to use for authentication.
        intents: Intents to use for the client.
        dispatcher: Event dispatcher.
        is_started: Whether the client is started.
    """

    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession,
        intents: Intent = DEFAULT_INTENTS,
        allowed_events: Sequence[type[GatewayEvent]] | None = None,
        ws_url: StrOrURL = GATEWAY_URL,
    ):
        """Initialize client.

        Args:
            token: Token to use for authentication.
            session: Session to use for requests.
            intents: Intents to use for the client.
            allowed_events: Events to allow.
            ws_url: URL to connect to. Defaults to the Discord Gateway URL.
        """
        self.token = token
        self.intents = intents
        self.dispatcher = EventDispatcher()
        self.dispatcher.add_argument('gateway', self)
        self.is_started = False

        self._ws_url = ws_url
        self._resume_url = None

        if allowed_events is not None:
            self._allowed_events = {event.__event_name__ for event in allowed_events}
        else:
            self._allowed_events = None

        self._session_id = None
        self._last_seq_number = 0
        self._session = session
        self._heartbeat = Heartbeat(self.heartbeat, self._handle_heartbeat_timeout)

    async def start(self) -> None:
        """Start the gateway client."""
        self.is_started = True
        async with self._session.ws_connect(self.url) as ws:
            self.ws = ws
            if logger.isEnabledFor(logging.DEBUG):
                logger.info('Connected to gateway at %s', self.url)
            else:
                logger.info('Connected to gateway')

            try:
                await self._ws_loop(ws)
            except (
                aiohttp.ClientConnectorError,
                errors.HeartbeatAckTimeoutError,
                errors.InvalidSessionError,
            ) as err:
                logger.error(err)
                await asyncio.sleep(5)

            except errors.NecessaryReconnectError:
                logger.info('Reconnect is necessary')

            except asyncio.CancelledError:
                logger.info('Gateway stopping')
                await self.stop()
                logger.info('Gateway stopped')

            except Exception as err:
                logger.exception('Unhandled exception in gateway loop: %s', err)
                raise

    async def stop(self) -> None:
        """Stop the gateway client."""
        await self._heartbeat.stop()
        if self.ws:
            await self.ws.close()
            self.ws = None
        self.is_started = False

    def add_handler[EVENT_T: GatewayEvent](self, event_handler: EventHandlerType[EVENT_T]) -> None:
        """Add an event handler.

        Args:
            event_handler: Event handler to add.
        """
        self.dispatcher.add_handler(event_handler)

    async def identify(self, command_data: IdentifyCommand) -> None:
        """Identify with the gateway.

        Args:
            command_data: Data to send to the gateway.
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
            presence_data: Data to send to the gateway.
        """
        prepared_data = presence_data.model_dump(mode='json')
        await self._send_command(GatewayCommandOpcode.PRESENCE_UPDATE, prepared_data)

    @property
    def url(self) -> StrOrURL:
        """Return the URL of the websocket connection.

        Returns:
            URL of the websocket connection.
        """
        return self._resume_url or self._ws_url

    async def _ws_loop(self, ws: ClientWebSocketResponse) -> None:
        while self.is_started:
            msg = await ws.receive()

            match msg.type:
                case WSMsgType.TEXT:
                    body = msg.json()
                    gw_message = GatewayMessageAdapter.model_validate(body)
                    await self._handle_message(gw_message)

                case WSMsgType.CLOSE | WSMsgType.CLOSING | WSMsgType.CLOSED:
                    logger.info(f'Connection closed: {msg.data} {msg.extra}')
                    break

                case _:
                    logger.warning(f'Unhandled websocket message type: {msg.type}')

    async def _send_command(self, op: GatewayCommandOpcode, command_data: Any) -> None:  # noqa: ANN401
        """Send a command to the gateway.

        Args:
            op: Opcode of the command.
            command_data: Command data to send.

        Raises:
            RuntimeError: If the client is not connected.
        """
        if not self.ws:
            raise RuntimeError('Client is not connected')
        await self.ws.send_json({'op': op, 'd': command_data})

    async def _handle_message(self, msg: GatewayMessageAdapter) -> None:
        """Handle a message from the gateway.

        This method is responsible for dispatching events to the registered handlers.

        Args:
            msg: Message to handle.

        Raises:
            InvalidSessionError: If the session is invalid.
        """
        logger.debug('Got message:\n%s', pretty_repr(msg))
        self._last_seq_number = max(self._last_seq_number, msg.sequence_number or 0)

        match msg.opcode:
            case GatewayMessageOpcode.DISPATCH:
                casted_event_name = cast(str, msg.event_name)
                if self._allowed_events is not None:
                    if casted_event_name not in self._allowed_events:
                        logger.debug('Event %s not allowed', casted_event_name)
                        return
                event_class = EVENT_MAP.get(casted_event_name)
                if event_class:
                    try:
                        event = event_class.model_validate(msg.data)
                    except ValidationError as err:
                        logger.exception(err)
                        return
                    if isinstance(event, ReadyEvent):
                        self._resume_url = event.resume_gateway_url
                        self._session_id = event.session_id

                    await self.dispatcher.dispatch(event)
                elif logger.isEnabledFor(logging.DEBUG):
                    logger.warning("Event '%s' unhandled", msg.event_name)

            case GatewayMessageOpcode.INVALID_SESSION:
                session_id = cast(str, self._session_id)
                self._session_id = None
                self._last_seq_number = 0
                raise errors.InvalidSessionError(session_id)

            case GatewayMessageOpcode.HELLO:
                event = HelloEvent.model_validate(msg.data)
                await self._hello(event)

            case GatewayMessageOpcode.HEARTBEAT_ACK:
                await self._heartbeat.ack()

            case GatewayMessageOpcode.RECONNECT:
                self._session_id = None
                self._last_seq_number = 0
                raise errors.NecessaryReconnectError

            case _:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.warning('Unhandled message:\n%s', pretty_repr(msg))

    async def _hello(self, event: HelloEvent) -> None:
        """Handle a hello event.

        Args:
            event: Event to handle.
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
