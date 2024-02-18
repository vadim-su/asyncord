from __future__ import annotations

import asyncio
import logging
from types import MappingProxyType
from typing import Any, Awaitable, Callable, Mapping, Protocol

import aiohttp
from pydantic import BaseModel
from rich.pretty import pretty_repr
from yarl import URL

from asyncord.gateway.client import errors
from asyncord.gateway.client.heartbeat import Heartbeat
from asyncord.gateway.commands import IdentifyCommand, PresenceUpdateData, ResumeCommand
from asyncord.gateway.dispatcher import EventDispatcher
from asyncord.gateway.events.base import ReadyEvent
from asyncord.gateway.events.event_map import EVENT_MAP
from asyncord.gateway.intents import DEFAULT_INTENTS, Intent
from asyncord.gateway.messages.message import (
    DatalessMessage,
    DispatchMessage,
    GatewayCommandOpcode,
    GatewayMessageAdapter,
    GatewayMessageOpcode,
    GatewayMessageType,
    HelloMessage,
)
from asyncord.logger import NameLoggerAdapter
from asyncord.urls import GATEWAY_URL

logger = logging.getLogger(__name__)


type HandlerMethod[HANDLER_MESSAGE: GatewayMessageType] = Callable[[HANDLER_MESSAGE], Awaitable[None]]
"""Type of a handler method for a specific message type."""


class GatewayClient:
    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession,
        conn_data: ConnectionData | None = None,
        intents: Intent = DEFAULT_INTENTS,
        heartbeat_class: type[HeartbeatProtocol] | HeartbeatFactoryProtocol = Heartbeat,
        dispatcher: EventDispatcher | None = None,
        name: str | None = None,
    ):
        self.token = token
        self.session = session
        self.conn_data = conn_data or ConnectionData(token=token)
        self.intents = intents
        self.heartbeat = heartbeat_class(self, self.conn_data)
        self.dispatcher = dispatcher or EventDispatcher()

        self.is_started = False
        self.name = name

        if self.name:
            self.logger = NameLoggerAdapter(logger, self.name)
        else:
            self.logger = logger

        self._ws = None
        self._need_restart = asyncio.Event()
        self._opcode_handlers: Mapping[GatewayMessageOpcode, HandlerMethod] = MappingProxyType({
            GatewayMessageOpcode.DISPATCH: self._handle_dispatch,
            GatewayMessageOpcode.RECONNECT: self._handle_reconnect,
            GatewayMessageOpcode.INVALID_SESSION: self._handle_invalid_session,
            GatewayMessageOpcode.HELLO: self._handle_hello,
            GatewayMessageOpcode.HEARTBEAT_ACK: self._handle_heartbeat_ack,
        })

    async def connect(self) -> None:
        """Connect to the gateway."""
        if self.is_started:
            raise RuntimeError('Client is already started')

        self.is_started = True

        await asyncio.shield(self._connect())

    async def close(self) -> None:
        """Stop the client."""
        self.logger.info('Closing gateway client')
        if not self.is_started or not self._ws:
            return

        self.is_started = False
        self._need_restart.set()
        self.heartbeat.stop()
        await self._ws.close()
        self.logger.info('Gateway client closed')

    async def send_command(self, opcode: GatewayCommandOpcode, data: Any) -> None:
        """Send a command to the gateway.

        Args:
            op: Opcode of the command.
            command_data: Command data to send.

        Raises:
            RuntimeError: If the client is not connected.
        """
        if not self._ws:
            raise RuntimeError('Client is not connected')
        await self._ws.send_json({'op': opcode, 'd': data})

    def reconnect(self) -> None:
        """Reconnect to the gateway.

        Close the current connection. If the client is started, then it will
        automatically reconnect.
        """
        if not self._ws:
            raise RuntimeError('Client is not started')

        self.heartbeat.stop()
        self._need_restart.set()

    async def identify(self, command_data: IdentifyCommand) -> None:
        """Identify with the gateway.

        Args:
            command_data: Data to send to the gateway.
        """
        payload = command_data.model_dump(mode='json', exclude_none=True)
        await self.send_command(GatewayCommandOpcode.IDENTIFY, payload)

    async def send_heartbeat(self, seq: int | None) -> None:
        """Send a heartbeat to the gateway."""
        await self.send_command(GatewayCommandOpcode.HEARTBEAT, seq)

    async def send_resume(self, command_data: ResumeCommand) -> None:
        """Resume a previous session.

        Args:
            command_data(ResumeCommand): Data to send to the gateway.
        """
        payload = command_data.model_dump(mode='json')
        await self.send_command(GatewayCommandOpcode.RESUME, payload)

    async def update_presence(self, presence_data: PresenceUpdateData) -> None:
        """Update the client's presence.

        Args:
            presence_data: Data to send to the gateway.
        """
        prepared_data = presence_data.model_dump(mode='json')
        await self.send_command(GatewayCommandOpcode.PRESENCE_UPDATE, prepared_data)

    async def _connect(self) -> None:
        while self.is_started:
            self._need_restart.clear()

            url = self.conn_data.resume_url
            async with self.session.ws_connect(url) as ws:
                self._ws = ws
                try:
                    await self._ws_recv_loop(ws)
                except errors.ConnectionClosed as err:
                    # if the connection is closed, then the client should try to reconnect
                    # if the client is still started
                    # we can get here if the connection is closed by the user too
                    self.logger.info(str(err))

            if self.is_started:
                self.logger.info('Reconnecting in 3 seconds')
                await asyncio.sleep(3)

    async def _handle_dispatch(self, message: DispatchMessage) -> None:
        self.conn_data.seq = max(self.conn_data.seq, message.sequence_number)

        if message.event_name == ReadyEvent.__event_name__:
            event = ReadyEvent.model_validate(message.data)
            await self._handle_ready(event)

        event_type = EVENT_MAP.get(message.event_name)
        if not event_type:
            self.logger.warning('Unhandled event: %s', message.event_name)
            return

        event = event_type.model_validate(message.data)
        await self.dispatcher.dispatch(event)

    async def _handle_reconnect(self, _: DatalessMessage) -> None:
        self.reconnect()

    async def _handle_invalid_session(self, _: GatewayMessageType) -> None:
        """Handle the invalid session event.

        Can be caused by a bad session ID or a session timeout or something else
        with concurrent connections.
        Also called if the seq number isn't changed between READY and RESUMED.
        """
        self.conn_data.reset()
        self.reconnect()

    async def _handle_hello(self, message: HelloMessage) -> None:
        """Handle the hello event."""
        self.heartbeat.run(message.data.heartbeat_interval)

        if self.conn_data.can_resume:
            self.logger.info('Resuming session %s', self.conn_data.session_id)
            # if should_resume, then all necessary data is present
            await self.send_resume(ResumeCommand(
                token=self.conn_data.token,
                session_id=self.conn_data.session_id,  # type: ignore
                seq=self.conn_data.seq,
            ))

        else:
            self.logger.info('Starting new session')
            await self.identify(IdentifyCommand(
                token=self.conn_data.token,
                intents=self.intents,
            ))

    async def _handle_ready(self, message: ReadyEvent) -> None:
        """Handle the ready event.

        Store the session ID and resume URL to resume the session later.
        """
        self.conn_data.session_id = message.session_id
        self.conn_data.resume_url = URL(message.resume_gateway_url)

    async def _handle_heartbeat_ack(self, _: DatalessMessage) -> None:
        await self.heartbeat.handle_heartbeat_ack()

    async def _ws_recv_loop(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        while self.is_started and not self._need_restart.is_set():
            msg_task = asyncio.create_task(self._get_message(ws), name='GatewayClient._get_message')
            need_restart_task = asyncio.create_task(
                self._need_restart.wait(), name='GatewayClient._need_restart.wait',
            )

            done, _ = await asyncio.wait(
                {msg_task, need_restart_task}, return_when=asyncio.FIRST_COMPLETED,
            )

            if need_restart_task in done:
                await need_restart_task
                if not msg_task.cancel():
                    await msg_task
                return

            need_restart_task.cancel()
            message = await msg_task
            if message:
                await self._handle_message(message)

    async def _get_message(self, ws: aiohttp.ClientWebSocketResponse) -> GatewayMessageType | None:
        """Get a message from the websocket."""

        msg = await ws.receive()
        if msg.type is aiohttp.WSMsgType.TEXT:
            data = msg.json()
            return GatewayMessageAdapter.validate_python(data)
        elif msg.type in {aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSED}:
            raise errors.ConnectionClosed
        else:
            self.logger.warning('Unhandled message type: %s', msg.type)
            return None

    async def _handle_message(self, message: GatewayMessageType) -> None:
        self.logger.info('Got message:\n%s', pretty_repr(message))

        opcode = message.opcode
        handler = self._opcode_handlers.get(opcode)
        if not handler:
            self.logger.warning('Unhandled opcode: %s', opcode)
            return

        await handler(message)


class ConnectionData(BaseModel, arbitrary_types_allowed=True):
    """Data used to connect or resume to the gateway."""

    token: str
    """Token used to connect to the gateway."""

    resume_url: URL = GATEWAY_URL
    """URL used to resume a previous session or connect to the gateway."""

    session_id: str | None = None
    """ID of the previous session."""

    seq: int = 0
    """Sequence number of the previous message."""

    @property
    def can_resume(self) -> bool:
        """Whether the connection data can be used to resume a session."""
        return all((self.resume_url, self.session_id, self.seq))

    def reset(self) -> None:
        """Reset the connection data."""
        self.resume_url = GATEWAY_URL
        self.session_id = None
        self.seq = 0


class HeartbeatProtocol(Protocol):
    """Protocol for the heartbeat class."""

    def __init__(self, client: GatewayClient, conn_data: ConnectionData) -> None:
        """Initialize the heartbeat."""

    async def handle_heartbeat_ack(self) -> None:
        """Handle a heartbeat ack."""

    def run(self, interval: int) -> None:
        """Run the heartbeat."""

    def stop(self) -> None:
        """Stop the heartbeat."""


class HeartbeatFactoryProtocol(Protocol):
    """Protocol for the heartbeat factory class."""

    def __call__(self, client: GatewayClient, conn_data: ConnectionData) -> HeartbeatProtocol:  # type: ignore
        """Create a heartbeat for the client."""
