"""This module contains the UserResource class, which is used to interact with."""

from __future__ import annotations

from asyncord.client.channels.models.output import ChannelOutput
from asyncord.client.members.models import MemberOutput
from asyncord.client.resources import ClientSubresource
from asyncord.client.users.models import UserGuildOutput, UserOutput
from asyncord.typedefs import LikeSnowflake, list_model
from asyncord.urls import REST_API_URL


class UserResource(ClientSubresource):
    """User resource.

    Attributes:
        users_url: Base users url.
        current_user_url: Current user url.
    """

    users_url = REST_API_URL / 'users'
    current_user_url = users_url / '@me'

    async def get_current_user(self) -> UserOutput:
        """Get the current user.

        Reference:
            https://discord.com/developers/docs/resources/user#modify-current-user
        """
        resp = await self._http_client.get(self.current_user_url)
        return UserOutput.model_validate(resp.body)

    async def get_user(self, user_id: LikeSnowflake) -> UserOutput:
        """Get a user.

        Reference: https://discord.com/developers/docs/resources/user#modify-current-user

        Args:
            user_id: ID of the user to get.
        """
        url = self.users_url / str(user_id)
        resp = await self._http_client.get(url)
        return UserOutput.model_validate(resp.body)

    async def update_user(self, username: str) -> UserOutput:
        """Update the current user.

        Args:
            username: New username.

        Reference: https://discord.com/developers/docs/resources/user#modify-current-user
        """
        payload = {'username': username}
        resp = await self._http_client.patch(self.current_user_url, payload)
        return UserOutput.model_validate(resp.body)

    async def get_guilds(
        self,
        before: LikeSnowflake | None = None,
        after: LikeSnowflake | None = None,
        limit: int | None = None,
    ) -> list[UserGuildOutput]:
        """Get the current user's guilds.

        This endpoint returns 200 guilds by default, which is the maximum
        number of guilds a non-bot user can join. Therefore, pagination is not needed
        for integrations that need to get a list of the users' guilds.

        Reference: 
        https://discord.com/developers/docs/resources/user#get-current-user-guilds

        Args:
            before: Get guilds before this guild ID.
            after: Get guilds after this guild ID.
            limit: Maximum number of guilds to get. Range: 1-200. Defaults to 200.

        Returns:
            Current user's guilds.
        """
        url_params = {}
        if before is not None:
            url_params['before'] = before
        if after is not None:
            url_params['after'] = after
        if limit is not None:
            url_params['limit'] = limit

        url = self.current_user_url / 'guilds' % url_params
        resp = await self._http_client.get(url)
        return list_model(UserGuildOutput).validate_python(resp.body)

    async def get_current_user_guild_member(self, guild_id: LikeSnowflake) -> MemberOutput:
        """Get the current user's guild member.

        Requires the guilds.members.read OAuth2 scope.

        Reference: https://discord.com/developers/docs/resources/user#get-current-user-guild-member

        Args:
            guild_id: ID of the guild.
        """
        url = self.current_user_url / f'guilds/{guild_id}/member'
        resp = await self._http_client.get(url)
        return MemberOutput.model_validate(resp.body)

    async def leave_guild(self, guild_id: LikeSnowflake) -> None:
        """Leave a guild.

        Reference: https://discord.com/developers/docs/resources/user#leave-guild

        Args:
            guild_id: ID of the guild to leave.
        """
        url = self.current_user_url / f'guilds/{guild_id}'
        await self._http_client.delete(url)

    async def create_dm(self, user_id: LikeSnowflake) -> ChannelOutput:
        """Create a DM with a user.

        Reference: https://discord.com/developers/docs/resources/user#create-dm

        Args:
            user_id: ID of the user to create a DM with.
        """
        url = self.current_user_url / 'channels'
        payload = {'recipient_id': user_id}
        resp = await self._http_client.post(url, payload)
        return ChannelOutput.model_validate(resp.body)

    async def create_group_dm(self, user_ids: list[LikeSnowflake]) -> ChannelOutput:
        """Create a group DM.

        This endpoint was intended to be used with the now-deprecated GameBridge SDK.
        DMs created with this endpoint will not be shown in the Discord client.

        Reference: https://discord.com/developers/docs/resources/user#create-group-dm

        Args:
            user_ids: IDs of the users to create a group DM with.
                The maximum number of users is 10.

        Returns:
            The created group DM.

        Raises:
            ValueError: If the number of users is greater than 10.
        """
        if len(user_ids) > 10:  # noqa: PLR2004
            # limited by discord to 10 users per group DM
            raise ValueError('Cannot create a group DM with more than 10 users.')
        url = self.current_user_url / 'channels'
        payload = {'recipient_ids': user_ids}
        resp = await self._http_client.post(url, payload)
        return ChannelOutput.model_validate(resp.body)
