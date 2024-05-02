"""This module contains the applications resource for the client."""

from asyncord.client.applications.models.requests import UpdateApplicationRequest
from asyncord.client.applications.models.responses import ApplicationOut
from asyncord.client.commands.resources import CommandResource
from asyncord.client.resources import ClientSubresource
from asyncord.snowflake import SnowflakeInputType
from asyncord.urls import REST_API_URL


class ApplicationResource(ClientSubresource):
    """Represents the applications resource for the client.

    Attributes:
        apps_url: URL for the applications resource.
    """

    apps_url = REST_API_URL / 'applications'

    def commands(self, app_id: SnowflakeInputType) -> CommandResource:
        """Get the commands resource for an application.

        Args:
            app_id: ID of the application.

        Returns:
            Commands resource.
        """
        return CommandResource(self, app_id)

    async def get_application(self) -> ApplicationOut:
        """Get the current application.

        Returns:
            Application object.
        """
        resp = await self._http_client.get(self.apps_url / '@me')
        return ApplicationOut.model_validate(resp.body)

    async def update_application(
        self,
        application_data: UpdateApplicationRequest,
    ) -> ApplicationOut:
        """Edit the current application.

        Args:
            application_data: Data to edit the application with.

        Returns:
            Application object.
        """
        payload = application_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(
            self.apps_url / '@me',
            payload=payload,
        )
        return ApplicationOut.model_validate(resp.body)
