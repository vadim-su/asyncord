"""This module contains the applications resource for the client."""

from asyncord.client.commands.resources import CommandResource
from asyncord.client.resources import ClientSubresource
from asyncord.typedefs import LikeSnowflake
from asyncord.urls import REST_API_URL


class ApplicationResource(ClientSubresource):
    """Represents the applications resource for the client.

    Attributes:
        apps_url: URL for the applications resource.
    """

    apps_url = REST_API_URL / 'applications'

    def commands(self, app_id: LikeSnowflake) -> CommandResource:
        """Get the commands resource for an application.

        Args:
            app_id: ID of the application.

        Returns:
            Commands resource.
        """
        return CommandResource(self, app_id)
