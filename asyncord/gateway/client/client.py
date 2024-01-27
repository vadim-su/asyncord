import aiohttp

from asyncord.gateway.client.commander import GatewayCommander
from asyncord.gateway.client.conn_data import ConnectionData
from asyncord.gateway.client.connection import GatewayConnection
from asyncord.gateway.client.handler import GatewayMessageHandler
from asyncord.gateway.commands import PresenceUpdateData
from asyncord.gateway.dispatcher import EventDispatcher, EventHandlerType
from asyncord.gateway.events.base import GatewayEvent
from asyncord.gateway.intents import DEFAULT_INTENTS, Intent


class GatewayClient:
    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession,
        conn_data: ConnectionData | None = None,
        intents: Intent = DEFAULT_INTENTS,
        dispatcher: EventDispatcher | None = None,
    ):
        self.token = token
        self.session = session
        self.conn_data = conn_data or ConnectionData(token=token)
        self.intents = intents

        self.conn = GatewayConnection(session, self.conn_data)
        self.commands = GatewayCommander(self.conn)

        if dispatcher:
            self.dispatcher = dispatcher
        else:
            self.dispatcher = EventDispatcher()
            self.dispatcher.add_argument('gateway', self)

        self.message_handler = GatewayMessageHandler(
            conn_data=self.conn_data,
            intents=self.intents,
            commands=self.commands,
            dispatcher=self.dispatcher,
        )

    async def start(self) -> None:
        """Start the client."""
        await self.conn.start(self.message_handler)

    async def stop(self) -> None:
        """Stop the client."""
        await self.conn.stop()

    def add_handler[EVENT_T: GatewayEvent](
        self, event_handler: EventHandlerType[EVENT_T],
    ) -> None:
        """Add a handler for a specific event type.

        Args:
            event_handler: Event handler to add.
        """
        self.dispatcher.add_handler(event_handler)

    async def update_presence(self, presence_data: PresenceUpdateData) -> None:
        """Update the client's presence.

        Args:
            presence_data: Data to send to the gateway.
        """
        await self.commands.update_presence(presence_data)
