"""Gateway client for the Discord API.

Contains the GatewayClient class which is used to connect to the Discord gateway.
Also contains some useful types and classes for the gateway client.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Mapping
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

import aiohttp
from pydantic import BaseModel
from yarl import URL

from asyncord.gateway.client import errors, opcode_handlers
from asyncord.gateway.client.heartbeat import Heartbeat
from asyncord.gateway.dispatcher import EventDispatcher
from asyncord.gateway.intents import DEFAULT_INTENTS
from asyncord.gateway.message import (
    DispatchMessage,
    GatewayCommandOpcode,
    GatewayMessageAdapter,
    GatewayMessageOpcode,
)
from asyncord.logger import NameLoggerAdapter
from asyncord.urls import GATEWAY_URL

if TYPE_CHECKING:
    from asyncord.client.http.middleware.auth import BotTokenAuthStrategy
    from asyncord.gateway.commands import IdentifyCommand, PresenceUpdateData, ResumeCommand
    from asyncord.gateway.intents import Intent
    from asyncord.gateway.message import DatalessMessage, GatewayMessageType

__all__ = (
    'ConnectionData',
    'GatewayClient',
    'HeartbeatFactoryProtocol',
    'HeartbeatProtocol',
)

logger = logging.getLogger(__name__)


class GatewayClient:
    """Client used to connect to the Discord gateway.

    It's main entity used to connect to the Discord gateway and send/proccess messages.
    """

    def __init__(
        self,
        *,
        token: str | BotTokenAuthStrategy,
        session: aiohttp.ClientSession,
        conn_data: ConnectionData | None = None,
        intents: Intent = DEFAULT_INTENTS,
        heartbeat_class: type[HeartbeatProtocol] | HeartbeatFactoryProtocol = Heartbeat,
        dispatcher: EventDispatcher | None = None,
        name: str | None = None,
    ):
        """Initialize the gateway client.

        Args:
            token: Token used to connect to the gateway.
            session: Client session used to connect to the gateway.
            conn_data: Data used to connect or resume to the gateway.
            intents: Intents to use for the client.
            heartbeat_class: Class used to create the heartbeat for the client.
            dispatcher: Event dispatcher used to dispatch events.
            name: Name of the client.
        """
        if not isinstance(token, str):
            token = token.token

        self.session = session
        self.conn_data = conn_data or ConnectionData(token=token)
        self.intents = intents
        if isinstance(heartbeat_class, HeartbeatFactoryProtocol):
            self.heartbeat = heartbeat_class.create(self, self.conn_data)
        else:
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
        self._opcode_handlers: Mapping[GatewayMessageOpcode, opcode_handlers.OpcodeHandler] = MappingProxyType({
            GatewayMessageOpcode.DISPATCH: opcode_handlers.DispatchHandler(self, self.logger),
            GatewayMessageOpcode.RECONNECT: opcode_handlers.ReconnectHandler(self, self.logger),
            GatewayMessageOpcode.INVALID_SESSION: opcode_handlers.InvalidSessionHandler(self, self.logger),
            GatewayMessageOpcode.HELLO: opcode_handlers.HelloHandler(self, self.logger),
            GatewayMessageOpcode.HEARTBEAT_ACK: opcode_handlers.HeartbeatAckHandler(self, self.logger),
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
        if not self.is_started and not self._ws:
            return

        self.is_started = False
        self._need_restart.set()
        self.heartbeat.stop()
        if self._ws:
            await self._ws.close()
        self._ws = None
        self.logger.info('Gateway client closed')

    async def send_command(self, opcode: GatewayCommandOpcode, data: Any) -> None:  # noqa: ANN401
        """Send a command to the gateway.

        Args:
            opcode: Opcode of the command.
            data: Data to send to the gateway.

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
            command_data: Data to send to the gateway.
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
            async with self.session.ws_connect(url=url) as ws:
                self._ws = ws
                try:
                    await self._ws_recv_loop(ws)
                except errors.ConnectionClosedError as err:
                    # if the connection is closed, then the client should try to reconnect
                    # if the client is still started
                    # we can get here if the connection is closed by the user too
                    self.logger.info(str(err))

            if self.is_started:
                self.logger.info('Reconnecting in 3 seconds')
                await asyncio.sleep(3)

    async def _handle_heartbeat_ack(self, _: DatalessMessage) -> None:
        await self.heartbeat.handle_heartbeat_ack()

    async def _ws_recv_loop(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        while self.is_started and not self._need_restart.is_set():
            msg_task = asyncio.create_task(self._get_message(ws), name='GatewayClient._get_message')
            need_restart_task = asyncio.create_task(
                self._need_restart.wait(),
                name='GatewayClient._need_restart.wait',
            )

            done, _ = await asyncio.wait(
                {msg_task, need_restart_task},
                return_when=asyncio.FIRST_COMPLETED,
            )

            if need_restart_task in done:
                await need_restart_task
                if not msg_task.cancel():
                    await msg_task
                return

            need_restart_task.cancel()
            message = await msg_task
            # when get ending message, message is None
            if message:
                await self._handle_message(message)

    async def _get_message(self, ws_resp: aiohttp.ClientWebSocketResponse) -> GatewayMessageType | None:
        """Get a message from the websocket."""
        msg = await ws_resp.receive()
        if msg.type is aiohttp.WSMsgType.TEXT:
            data = msg.json()
            return GatewayMessageAdapter.validate_python(data)

        if msg.type in {aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSED}:
            raise errors.ConnectionClosedError

        self.logger.warning('Unhandled message type: %s', msg.type)
        return None

    async def _handle_message(self, message: GatewayMessageType) -> None:
        if isinstance(message, DispatchMessage):
            self.logger.info('Dispatching event: %s', message.event_name)
        else:
            self.logger.info('Received message: %s', message.opcode.name)

        opcode = message.opcode
        handler = self._opcode_handlers.get(opcode)
        if not handler:
            self.logger.warning('Unhandled opcode: %s', opcode)
            return

        await handler.handle(message)


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


@runtime_checkable
class HeartbeatFactoryProtocol(Protocol):
    """Protocol for the heartbeat factory class."""

    def create(self, client: GatewayClient, conn_data: ConnectionData) -> HeartbeatProtocol:
        """Create a heartbeat instance."""
        ...
