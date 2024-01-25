import aiohttp

from asyncord.gateway.client.commander import GatewayCommander
from asyncord.gateway.client.conn_data import ConnectionData
from asyncord.gateway.client.connection import GatewayConnection
from asyncord.gateway.client.handler import GatewayMessageHandler
from asyncord.gateway.commands import PresenceUpdateData
from asyncord.gateway.intents import DEFAULT_INTENTS, Intent


class GatewayClient:
    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession,
        conn_data: ConnectionData | None = None,
        intents: Intent = DEFAULT_INTENTS,
    ):
        self.token = token
        self.session = session
        self.conn_data = conn_data or ConnectionData(token=token)
        self.intents = intents

        self.conn = GatewayConnection(session, self.conn_data)
        self.commands = GatewayCommander(self.conn)
        self.message_handler = GatewayMessageHandler(
            conn_data=self.conn_data,
            intents=self.intents,
            commands=self.commands,
        )

    async def start(self) -> None:
        """Start the client."""
        await self.conn.start(self.message_handler)

    async def stop(self) -> None:
        """Stop the client."""
        self.is_started = False

    async def update_presence(self, presence_data: PresenceUpdateData) -> None:
        """Update the client's presence.

        Args:
            presence_data: Data to send to the gateway.
        """
        await self.commands.update_presence(presence_data)
