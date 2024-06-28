"""This module contains role resource classes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.resources import APIResource
from asyncord.client.roles.models.requests import RolePositionRequest
from asyncord.client.roles.models.responses import RoleResponse
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.client.roles.models.requests import CreateRoleRequest, UpdateRoleRequest
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('RoleResource',)


class RoleResource(APIResource):
    """Resource to perform actions on roles.

    Attributes:
        guild_id: ID of the guild.
    """

    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, http_client: HttpClient, guild_id: SnowflakeInputType):
        """Initialize the role resource."""
        super().__init__(http_client)
        self.guild_id = guild_id
        self.roles_url = self.guilds_url / str(self.guild_id) / 'roles'

    async def get_list(self) -> list[RoleResponse]:
        """Get a list of roles in a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-roles

        Returns:
            List of roles in the guild.
        """
        resp = await self._http_client.get(url=self.roles_url)
        return list_model(RoleResponse).validate_python(resp.body)

    async def create(
        self,
        role_data: CreateRoleRequest,
        reason: str | None = None,
    ) -> RoleResponse:
        """Create a new role in a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#create-guild-role

        Args:
            role_data: Data for the role to create.
            reason: Reason for creating the role.

        Returns:
            Created role.
        """
        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = role_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url=self.roles_url, payload=payload, headers=headers)
        return RoleResponse.model_validate(resp.body)

    async def change_role_positions(self, role_positions: list[RolePositionRequest]) -> list[RoleResponse]:
        """Change the position of a role in a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#modify-guild-role-positions

        Args:
            role_positions: List of role positions to change.

        Returns:
            List of roles in the guild.
        """
        payload = list_model(RolePositionRequest).dump_python(role_positions, mode='json')

        resp = await self._http_client.patch(url=self.roles_url, payload=payload)
        return list_model(RoleResponse).validate_python(resp.body)

    async def update_role(self, role_id: SnowflakeInputType, role_data: UpdateRoleRequest) -> RoleResponse:
        """Update a role in a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#modify-guild-role

        Args:
            role_id: ID of the role to update.
            role_data: Data for the role to update.

        Returns:
            Updated role.
        """
        url = self.roles_url / str(role_id)
        payload = role_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(url=url, payload=payload)
        return RoleResponse.model_validate(resp.body)

    async def delete(self, role_id: SnowflakeInputType, reason: str | None = None) -> None:
        """Delete a role in a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#delete-guild-role

        Args:
            role_id: ID of the role to delete.
            reason: Reason for deleting the role.
        """
        url = self.roles_url / str(role_id)
        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url=url, headers=headers)
