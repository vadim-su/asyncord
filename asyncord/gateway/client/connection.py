from __future__ import annotations

import asyncio
import logging
from typing import Any, Protocol

import aiohttp
from yarl import URL

from asyncord.gateway.client.conn_data import ConnectionData
from asyncord.gateway.messages.message import GatewayCommandOpcode, GatewayMessageAdapter, GatewayMessageType
from asyncord.urls import GATEWAY_URL

logger = logging.getLogger(__name__)


class GatewayConnection:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        conn_data: ConnectionData,
        gw_url: URL = GATEWAY_URL,
    ):
        self.session = session
        self.resume_data = conn_data
        self.gw_url = gw_url

        self.is_started = False
        self.ws = None

    async def start(self, handler: GatewayHandlerProtocol) -> None:
        """Start the client."""
        if self.is_started:
            raise RuntimeError('Client is already started')

        self.is_started = True
        url = self.resume_data.resume_url or self.gw_url

        while self.is_started:
            try:
                async with self.session.ws_connect(url) as ws:
                    self.ws = ws
                    await self._ws_recv_loop(ws, handler)

            except aiohttp.ClientError:
                logger.exception('Error while connecting to gateway')
                await asyncio.sleep(5)

    async def stop(self) -> None:
        """Stop the client."""
        if not self.is_started or not self.ws:
            raise RuntimeError('Client is not started')
        self.is_started = False
        await self.ws.close()
        self.ws = None

    async def send_command(self, op: GatewayCommandOpcode, command_data: Any) -> None:  # noqa: ANN401
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

    async def _ws_recv_loop(self, ws: aiohttp.ClientWebSocketResponse, handler: GatewayHandlerProtocol) -> None:
        async for msg in ws:
            if not self.is_started:
                break

            if msg.type is aiohttp.WSMsgType.TEXT:
                data = msg.json()
                message = GatewayMessageAdapter.validate_python(data)
                await handler.handle_message(message)

        else:
            logger.info('Gateway connection closed.')


class GatewayHandlerProtocol(Protocol):
    async def handle_message(self, message: GatewayMessageType) -> None:
        ...
