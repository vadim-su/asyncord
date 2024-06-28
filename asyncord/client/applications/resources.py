"""This module contains the applications resource for the client."""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.applications.models.responses import ApplicationOut, ApplicationRoleConnectionMetadataOut
from asyncord.client.commands.resources import CommandResource
from asyncord.client.resources import APIResource
from asyncord.typedefs import CURRENT_USER, list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.applications.models.requests import (
        UpdateApplicationRequest,
        UpdateApplicationRoleConnectionMetadataRequest,
    )
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('ApplicationResource',)


class ApplicationResource(APIResource):
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
        return CommandResource(self._http_client, app_id)

    async def get_application(self) -> ApplicationOut:
        """Get the current application.

        Returns:
            Application object.
        """
        resp = await self._http_client.get(url=self.apps_url / CURRENT_USER)
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
            url=self.apps_url / CURRENT_USER,
            payload=payload,
        )
        return ApplicationOut.model_validate(resp.body)

    async def get_application_role_connection_metadata_records(
        self,
        app_id: SnowflakeInputType,
    ) -> list[ApplicationRoleConnectionMetadataOut]:
        """Get the role connection metadata records for an application.

        Args:
            app_id: ID of the application.

        Returns:
            List of application role connection metadata objects.
        """
        resp = await self._http_client.get(
            url=self.apps_url / str(app_id) / 'role-connections/metadata',
        )
        return list_model(ApplicationRoleConnectionMetadataOut).validate_python(resp.body)

    async def update_application_role_connection_metadata_records(
        self,
        app_id: SnowflakeInputType,
        apllication_role_metadata: UpdateApplicationRoleConnectionMetadataRequest,
    ) -> list[ApplicationRoleConnectionMetadataOut]:
        """Update the role connection metadata records for an application.

        Args:
            app_id: ID of the application.
            apllication_role_metadata: Application role connection metadata object.

        Returns:
            List of application role connection metadata objects.
        """
        payload = apllication_role_metadata.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(
            url=self.apps_url / str(app_id) / 'role-connections/metadata',
            payload=payload,
        )

        return list_model(ApplicationRoleConnectionMetadataOut).validate_python(resp.body)
