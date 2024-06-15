"""Opcode handlers for the gateway client.

These handlers are used to handle the different opcodes received from the gateway.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

from yarl import URL

from asyncord.gateway.commands import IdentifyCommand, ResumeCommand
from asyncord.gateway.events.base import ReadyEvent
from asyncord.gateway.events.event_map import EVENT_MAP
from asyncord.gateway.message import GatewayMessageOpcode

if TYPE_CHECKING:
    from asyncord.gateway.client.client import GatewayClient
    from asyncord.gateway.message import (
        DatalessMessage,
        DispatchMessage,
        GatewayMessageType,
        InvalidSessionMessage,
    )

__all__ = (
    'DispatchHandler',
    'HeartbeatAckHandler',
    'HelloHandler',
    'InvalidSessionHandler',
    'OpcodeHandler',
    'ReconnectHandler',
)


class OpcodeHandler(ABC):
    """Base class for opcode handlers.

    Attributes:
        opcode:  Opcode to handle.
        client:  Gateway client.
        logger:  Logger.
    """

    opcode: ClassVar[GatewayMessageOpcode]

    def __init__(self, client: GatewayClient, logger: logging.Logger | logging.LoggerAdapter):
        """Initialize opcode handler.

        Args:
            client:  Gateway client.
            logger:  Logger or logger adapter.
                We can use a logger adapter to include the client's name in the log messages.
        """
        self.client = client
        self.logger = logger

    @abstractmethod
    async def handle(self, message: GatewayMessageType) -> None:
        """Handle the message."""
        raise NotImplementedError('handle method must be implemented')


class DispatchHandler(OpcodeHandler):
    """Handle DISPATCH opcode."""

    opcode = GatewayMessageOpcode.DISPATCH

    async def handle(self, message: DispatchMessage) -> None:
        """Handle the DISPATCH opcode."""
        client = self.client
        client.conn_data.seq = max(client.conn_data.seq, message.sequence_number)

        if message.event_name == ReadyEvent.__event_name__:
            event = ReadyEvent.model_validate(message.data)
            await self._handle_ready(event)

        event_type = EVENT_MAP.get(message.event_name)
        if not event_type:
            self.logger.warning('Unhandled event: %s', message.event_name)
            return

        event = event_type.model_validate(message.data)
        await client.dispatcher.dispatch(event)

    async def _handle_ready(self, message: ReadyEvent) -> None:
        """Handle the ready event.

        Store the session ID and resume URL to resume the session later.
        """
        self.client.conn_data.session_id = message.session_id
        self.client.conn_data.resume_url = URL(message.resume_gateway_url)


class ReconnectHandler(OpcodeHandler):
    """Handle RECONNECT opcode."""

    opcode = GatewayMessageOpcode.RECONNECT

    async def handle(self, _message: DatalessMessage) -> None:
        """Handle the RECONNECT opcode."""
        self.logger.info('Received RECONNECT opcode. Reconnecting...')
        self.client.reconnect()


class InvalidSessionHandler(OpcodeHandler):
    """Handle INVALID_SESSION opcode."""

    opcode = GatewayMessageOpcode.INVALID_SESSION

    async def handle(self, message: InvalidSessionMessage) -> None:
        """Handle the INVALID_SESSION opcode."""
        if message.data:
            self.logger.info('Received INVALID_SESSION opcode. Reconnecting...')
        else:
            self.logger.info('Received INVALID_SESSION opcode. Resuming...')
            self.client.conn_data.reset()

        self.client.reconnect()


class HelloHandler(OpcodeHandler):
    """Handle HELLO opcode."""

    opcode = GatewayMessageOpcode.HELLO

    async def handle(self, _message: DatalessMessage) -> None:
        """Handle the HELLO opcode."""
        self.logger.info('Received HELLO opcode')

        self.client.heartbeat.run(interval=41250)

        if self.client.conn_data.can_resume:
            self.logger.info("Resuming session '%s'...", self.client.conn_data.session_id)
            await self.client.send_resume(
                ResumeCommand(
                    token=self.client.conn_data.token,
                    session_id=self.client.conn_data.session_id,  # type: ignore
                    seq=self.client.conn_data.seq,
                ),
            )
        else:
            self.logger.info('Starting new session')
            await self.client.identify(
                IdentifyCommand(
                    token=self.client.conn_data.token,
                    intents=self.client.intents,
                ),
            )


class HeartbeatAckHandler(OpcodeHandler):
    """Handle HEARTBEAT_ACK opcode."""

    opcode = GatewayMessageOpcode.HEARTBEAT_ACK

    async def handle(self, _message: DatalessMessage) -> None:
        """Handle the HEARTBEAT_ACK opcode."""
        self.logger.debug('Received HEARTBEAT_ACK opcode')
        await self.client.heartbeat.handle_heartbeat_ack()
