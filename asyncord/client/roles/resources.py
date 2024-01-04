"""This module contains role resource classes."""

from __future__ import annotations

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.resources import ClientResource, ClientSubresource
from asyncord.client.roles.models import CreateRoleData, Role, RolePosition, UpdateRoleData
from asyncord.typedefs import LikeSnowflake, list_model
from asyncord.urls import REST_API_URL


class RoleResource(ClientSubresource):
    """Resource to perform actions on roles.

    Attributes:
        guild_id: ID of the guild.
    """

    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, parent: ClientResource, guild_id: LikeSnowflake):
        """Initialize the role resource."""
        super().__init__(parent)
        self.guild_id = guild_id
        self.roles_url = self.guilds_url / str(self.guild_id) / 'roles'

    async def get_list(self) -> list[Role]:
        """Get a list of roles in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-roles

        Returns:
            List of roles in the guild.
        """
        resp = await self._http_client.get(self.roles_url)
        return list_model(Role).validate_python(resp.body)

    async def create(self, role_data: CreateRoleData) -> Role:
        """Create a new role in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#create-guild-role

        Args:
            role_data: Data for the role to create.

        Returns:
            Created role.
        """
        payload = role_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(self.roles_url, payload)
        return Role.model_validate(resp.body)

    async def change_role_positions(self, role_positions: list[RolePosition]) -> list[Role]:
        """Change the position of a role in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#modify-guild-role-positions

        Args:
            role_positions: List of role positions to change.

        Returns:
            List of roles in the guild.
        """
        resp = await self._http_client.patch(self.roles_url, role_positions)
        return list_model(Role).validate_python(resp.body)

    async def update_role(self, role_id: LikeSnowflake, role_data: UpdateRoleData) -> Role:
        """Update a role in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#modify-guild-role

        Args:
            role_id: ID of the role to update.
            role_data: Data for the role to update.

        Returns:
            Updated role.
        """
        url = self.roles_url / str(role_id)
        payload = role_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(url, payload)
        return Role.model_validate(resp.body)

    async def delete(self, role_id: LikeSnowflake, reason: str | None = None) -> None:
        """Delete a role in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#delete-guild-role

        Args:
            role_id: ID of the role to delete.
            reason: Reason for deleting the role.
        """
        url = self.roles_url / str(role_id)
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url, headers=headers)
