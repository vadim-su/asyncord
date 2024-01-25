from asyncord.gateway.client.connection import GatewayConnection
from asyncord.gateway.commands import IdentifyCommand, PresenceUpdateData, ResumeCommand
from asyncord.gateway.messages.message import GatewayCommandOpcode


class GatewayCommander:
    """Commands used to interact with the gateway."""

    def __init__(self, conn: GatewayConnection):
        self.conn = conn

    async def identify(self, command_data: IdentifyCommand) -> None:
        """Identify with the gateway.

        Args:
            command_data: Data to send to the gateway.
        """
        payload = command_data.model_dump(mode='json', exclude_none=True)
        await self.conn.send_command(GatewayCommandOpcode.IDENTIFY, payload)

    async def heartbeat(self) -> None:
        """Send a heartbeat to the gateway."""
        await self.conn.send_command(GatewayCommandOpcode.HEARTBEAT, None)

    async def resume(self, command_data: ResumeCommand) -> None:
        """Resume a previous session.

        Args:
            command_data(ResumeCommand): Data to send to the gateway.
        """
        await self.conn.send_command(GatewayCommandOpcode.RESUME, command_data.model_dump(mode='json'))

    async def update_presence(self, presence_data: PresenceUpdateData) -> None:
        """Update the client's presence.

        Args:
            presence_data: Data to send to the gateway.
        """
        prepared_data = presence_data.model_dump(mode='json')
        await self.conn.send_command(GatewayCommandOpcode.PRESENCE_UPDATE, prepared_data)
