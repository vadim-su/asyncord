"""This module containing the command resources.

Reference:
https://discord.com/developers/docs/interactions/slash-commands#applicationcommand
"""

from asyncord.client.models.commands import ApplicationCommand, CreateApplicationCommandData
from asyncord.client.resources import ClientResource, ClientSubresources
from asyncord.typedefs import LikeSnowflake, list_model
from asyncord.urls import REST_API_URL


class BaseCommandResource(ClientSubresources):
    """Base class for command resources.

    Attributes:
        applications_url: Base applications url.
    """

    applications_url = REST_API_URL / 'applications'

    def __init__(self, parent: ClientResource, app_id: LikeSnowflake) -> None:
        """Initialize the command resource."""
        super().__init__(parent)
        self.app_id = app_id
        self.commands_url = self.applications_url / str(app_id) / 'commands'

    async def get(self, command_id: LikeSnowflake) -> ApplicationCommand:
        """Get a command by id.

        Args:
            command_id: ID of the command to get.

        Returns:
            Object of the command.
        """
        url = self.commands_url / str(command_id)
        resp = await self._http.get(url)
        return ApplicationCommand.model_validate(resp.body)

    async def get_list(self) -> list[ApplicationCommand]:
        """Get a list of commands.

        Returns:
            List of commands.
        """
        resp = await self._http.get(self.commands_url)
        return list_model(ApplicationCommand).validate_python(resp.body)

    async def create(self, command_data: CreateApplicationCommandData) -> ApplicationCommand:
        """Create a command.

        If a command with the same name already exists, it will be overwritten.

        Args:
            command_data: Command to create.

        Returns:
            Created command.
        """
        payload = command_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http.post(self.commands_url, payload)
        return ApplicationCommand.model_validate(resp.body)

    async def delete(self, command_id: LikeSnowflake) -> None:
        """Delete a command.

        Args:
            command_id: ID of the command to delete.
        """
        url = self.commands_url / str(command_id)
        await self._http.delete(url)
