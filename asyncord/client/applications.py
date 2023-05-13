from asyncord.client.commands import BaseCommandResource
from asyncord.client.resources import ClientSubresources
from asyncord.typedefs import LikeSnowflake
from asyncord.urls import REST_API_URL


class ApplicationResource(ClientSubresources):

    apps_url = REST_API_URL / 'applications'

    def commands(self, app_id: LikeSnowflake) -> BaseCommandResource:
        """Get the commands resource for an application.

        Args:
            app_id (LikeSnowflake): Id of the application.

        Returns:
            BaseCommandsResource: commands resource.
        """
        return BaseCommandResource(self, app_id)
