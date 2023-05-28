from __future__ import annotations

from pydantic import TypeAdapter

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.models.roles import CreateRoleData, Role, RolePosition, UpdateRoleData
from asyncord.client.resources import ClientResource, ClientSubresources
from asyncord.typedefs import LikeSnowflake
from asyncord.urls import REST_API_URL


class RoleResource(ClientSubresources):
    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, parent: ClientResource, guild_id: LikeSnowflake):
        super().__init__(parent)
        self.guild_id = guild_id
        self.roles_url = self.guilds_url / str(self.guild_id) / 'roles'

    async def get_list(self) -> list[Role]:
        """Get a list of roles in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-roles

        Returns:
            list[Role]: The list of roles in the guild.
        """
        resp = await self._http.get(self.roles_url)
        return _RoleListValidator.validate_python(resp.body)

    async def create(self, role_data: CreateRoleData) -> Role:
        """Create a new role in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#create-guild-role

        Args:
            role_data (CreateRoleData): The data for the role to create.

        Returns:
            Role: The created role.
        """
        payload = role_data.dict(exclude_unset=True)
        resp = await self._http.post(self.roles_url, payload)
        return Role.model_validate(resp.body)

    async def change_role_positions(self, role_positions: list[RolePosition]) -> list[Role]:
        """Change the position of a role in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#modify-guild-role-positions

        Args:
            role_positions (list[RolePosition]): The list of role positions to change.

        Returns:
            list[Role]: The list of roles in the guild.
        """
        resp = await self._http.patch(self.roles_url, role_positions)
        return _RoleListValidator.validate_python(resp.body)

    async def update_role(self, role_id: LikeSnowflake, role_data: UpdateRoleData) -> Role:
        """Update a role in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#modify-guild-role

        Args:
            role_id (LikeSnowflake): The ID of the role to update.
            role_data (UpdateRoleData): The data for the role to update.

        Returns:
            Role: The updated role.
        """
        url = self.roles_url / str(role_id)
        payload = role_data.dict(exclude_unset=True)
        resp = await self._http.patch(url, payload)
        return Role.model_validate(resp.body)

    async def delete(self, role_id: LikeSnowflake, reason: str | None = None) -> None:
        """Delete a role in a guild.

        Reference: https://discord.com/developers/docs/resources/guild#delete-guild-role

        Args:
            role_id (LikeSnowflake): The ID of the role to delete.
            reason (str | None): The reason for deleting the role.
        """
        url = self.roles_url / str(role_id)
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http.delete(url, headers=headers)


_RoleListValidator = TypeAdapter(list[Role])
