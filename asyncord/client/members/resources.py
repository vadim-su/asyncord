"""Members resource for the client."""

from __future__ import annotations

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.members.models.requests import UpdateMemberRequest
from asyncord.client.members.models.responses import MemberResponse
from asyncord.client.resources import ClientResource, ClientSubresource
from asyncord.snowflake import SnowflakeInputType
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL


class MemberResource(ClientSubresource):
    """Resource to perform actions on members.

    Attributes:
        guilds_url: URL for the guilds resource.
    """
    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, parent: ClientResource, guild_id: SnowflakeInputType):
        """Create a new member resource."""
        super().__init__(parent)
        self.guild_id = guild_id
        self.members_url = self.guilds_url / str(self.guild_id) / 'members'

    async def get(self, user_id: SnowflakeInputType) -> MemberResponse:
        """Get a member of a guild.

        This endpoint is restricted according to whether the GUILD_MEMBERS Privileged.

        Args:
            user_id: ID of the member to get.

        Returns:
            Member object for the ID provided.
        """
        url = self.members_url / str(user_id)
        resp = await self._http_client.get(url)
        return MemberResponse.model_validate(resp.body)

    async def get_list(self, limit: int | None = None, after: SnowflakeInputType | None = None) -> list[MemberResponse]:
        """List members of guild.

        This endpoint is restricted according to whether the GUILD_MEMBERS Privileged
        Intent is enabled for your application.

        Args:
            limit: Maximum number of members to return.
                Should be between 1 and 1000.
            after: ID of the member to start at.

        Returns:
            List of members.
        """
        url_params = {}
        if limit is not None:
            url_params['limit'] = limit
        if after is not None:
            url_params['after'] = after

        url = self.members_url % url_params
        resp = await self._http_client.get(url)
        return list_model(MemberResponse).validate_python(resp.body)

    async def search(self, nick_or_name: str, limit: int | None = None) -> list[MemberResponse]:
        """Search members of a guild by username or nickname.

        Args:
            nick_or_name: Name or nickname of the member to search for.
            limit: Maximum number of members to return.
                Should be between 1 and 1000.

        Returns:
            List of members.
        """
        url_params = {}
        if nick_or_name is not None:
            url_params['query'] = nick_or_name
        if limit is not None:
            url_params['limit'] = limit

        url = self.members_url % url_params
        resp = await self._http_client.get(url)
        return list_model(MemberResponse).validate_python(resp.body)

    async def update(
        self,
        user_id: SnowflakeInputType,
        member_data: UpdateMemberRequest,
        reason: str | None = None,
    ) -> MemberResponse:
        """Update a member.

        Args:
            user_id: ID of the member to update.
            member_data: Data to update.
            reason: Reason for the update. Defaults to None.

        Returns:
            The updated member.
        """
        url = self.members_url / str(user_id)
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        resp = await self._http_client.patch(url, member_data, headers=headers)
        return MemberResponse(**resp.body)

    async def update_current_member(
        self,
        nickname: str | None,
        reason: str | None = None,
    ) -> MemberResponse:
        """Update the current member.

        Args:
            nickname: Nickname to update to.
                None to reset to user's default nickname.
            reason: Reason for the update. Defaults to None.

        Returns:
            The updated member.
        """
        url = self.members_url / '@me'
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        payload = {'nick': nickname}
        resp = await self._http_client.patch(url, payload, headers=headers)
        return MemberResponse.model_validate(resp.body)

    async def add_role(
        self,
        user_id: SnowflakeInputType,
        role_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Add a role to a member.

        Args:
            user_id: ID of the member to add a role to.
            role_id: ID of the role to add.
            reason: Reason for adding the role to the member. Defaults to None.
        """
        url = self.members_url / str(user_id) / 'roles' / str(role_id)
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        await self._http_client.put(url, None, headers=headers)

    async def remove_role(
        self,
        user_id: SnowflakeInputType,
        role_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Remove a role from a member.

        Args:
            user_id: ID of the member to remove a role from.
            role_id: ID of the role to remove.
            reason: Reason for removing the role from the member. Defaults to None.
        """
        url = self.members_url / str(user_id) / 'roles' / str(role_id)
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        await self._http_client.delete(url, headers=headers)

    async def kick(self, user_id: SnowflakeInputType, reason: str | None = None) -> None:
        """Kick a member from the guild.

        Args:
            user_id: ID of the member to kick.
            reason: Reason for kicking the member. Defaults to None.
        """
        url = self.members_url / str(user_id)
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        await self._http_client.delete(url, headers=headers)