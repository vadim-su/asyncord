import logging

from rich.pretty import pretty_repr
from yarl import URL

from asyncord.gateway.client.commander import GatewayCommander
from asyncord.gateway.client.conn_data import ConnectionData
from asyncord.gateway.commands import IdentifyCommand, ResumeCommand
from asyncord.gateway.dispatcher import EventDispatcher
from asyncord.gateway.events.base import HelloEvent, ReadyEvent
from asyncord.gateway.events.event_map import EVENT_MAP
from asyncord.gateway.intents import Intent
from asyncord.gateway.messages.message import DatalessMessage, DispatchMessage, GatewayMessageOpcode, GatewayMessageType

logger = logging.getLogger(__name__)


class GatewayMessageHandler:
    def __init__(self, conn_data: ConnectionData, intents: Intent, commands: GatewayCommander, dispatcher: EventDispatcher):
        self.conn_data = conn_data
        self.intents = intents
        self.commands = commands
        self.dispatcher = dispatcher

        self.opcode_handlers = {
            GatewayMessageOpcode.DISPATCH: self._handle_dispatch,
            GatewayMessageOpcode.RECONNECT: self._handle_reconnect,
            GatewayMessageOpcode.INVALID_SESSION: self._handle_invalid_session,
            GatewayMessageOpcode.HELLO: self._handle_hello,
            GatewayMessageOpcode.HEARTBEAT_ACK: self._handle_heartbeat_ack,
        }

    async def handle_message(self, message: GatewayMessageType) -> bool:
        """Handle a gateway message.

        Args:
            message: Message to handle.

        Returns:
            Whethre the client should reconnect.
        """
        logger.debug('Got message:\n%s', pretty_repr(message))

        handler = self.opcode_handlers.get(message.opcode)
        if handler:
            return await handler(message)
        else:
            logger.warning('Unhandled message opcode: %s', message.opcode)

        return False

    async def _handle_dispatch(self, message: DispatchMessage) -> bool:
        self.conn_data.seq = max(self.conn_data.seq, message.sequence_number)

        if message.event_name == ReadyEvent.__event_name__:
            event = ReadyEvent.model_validate(message.data)
            await self._handle_ready(event)

        event_type = EVENT_MAP.get(message.event_name)
        if not event_type:
            logger.warning('Unhandled event: %s', message.event_name)
            return False

        event = event_type.model_validate(message.data)
        await self.dispatcher.dispatch(event)
        return False

    async def _handle_reconnect(self, _: DatalessMessage) -> bool:
        return True

    async def _handle_invalid_session(self, message: GatewayMessageType) -> bool:
        self.conn_data.session_id = None
        self.conn_data.seq = 0
        return True

    async def _handle_hello(self, message: HelloEvent) -> bool:
        if self.conn_data.should_resume:
            # if should_resume, then all necessary data is present
            await self.commands.resume(ResumeCommand(
                token=self.conn_data.token,   # type: ignore
                session_id=self.conn_data.session_id,  # type: ignore
                seq=self.conn_data.seq,   # type: ignore
            ))

        else:
            await self.commands.identify(IdentifyCommand(
                token=self.conn_data.token,
                intents=self.intents,
            ))

        return False

    async def _handle_ready(self, message: ReadyEvent) -> bool:
        """Handle the ready event.

        Store the session ID and resume URL to resume the session later.
        """
        self.conn_data.session_id = message.session_id
        self.conn_data.resume_url = URL(message.resume_gateway_url)
        return False

    async def _handle_heartbeat_ack(self, _: DatalessMessage) -> None:
        ...
