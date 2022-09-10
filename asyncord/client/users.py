from __future__ import annotations

from asyncord.urls import REST_API_URL
from asyncord.typedefs import LikeSnowflake
from asyncord.client.resources import ClientSubresources
from asyncord.client.http_proto import Response
from asyncord.client.models.users import User
from asyncord.client.models.guilds import PartialUserGuild
from asyncord.client.models.member import Member
from asyncord.client.models.channels import Channel


class UserResource(ClientSubresources):
    users_url = REST_API_URL / 'users'
    current_user_url = users_url / '@me'

    async def get_current_user(self) -> User:
        """Get the current user.

        Reference:
            https://discord.com/developers/docs/resources/user#modify-current-user
        """
        resp = await self._http.get(self.current_user_url)
        return User(**resp.body)

    async def get_user(self, user_id: LikeSnowflake) -> User:
        """Get a user.

        Reference: https://discord.com/developers/docs/resources/user#modify-current-user

        Arguments:
            user_id (LikeSnowflake): The ID of the user to get.
        """

        url = self.users_url / str(user_id)
        resp = await self._http.get(url)
        return User(**resp.body)

    async def update_user(self, username: str) -> Response:
        """Update the current user.

        Arguments:
            username (str): The new username.

        Reference: https://discord.com/developers/docs/resources/user#modify-current-user
        """
        payload = {'username': username}
        return await self._http.patch(self.current_user_url, payload)

    async def get_guilds(
        self,
        before: LikeSnowflake | None = None,
        after: LikeSnowflake | None = None,
        limit: int | None = None,
    ) -> list[PartialUserGuild]:
        """Get the current user's guilds.

        This endpoint returns 200 guilds by default, which is the maximum
        number of guilds a non-bot user can join. Therefore, pagination is not needed
        for integrations that need to get a list of the users' guilds.

        Reference: https://discord.com/developers/docs/resources/user#get-current-user-guilds

        Arguments:
            before (LikeSnowflake | None): Get guilds before this guild ID.
            after (LikeSnowflake | None): Get guilds after this guild ID.
            limit (int | None): The maximum number of guilds to get. Range: 1-200.
                 Defaults to 200.

        Returns:
            list[Guild]: The current user's guilds.
        """
        url_params = {}
        if before is not None:
            url_params['before'] = before
        if after is not None:
            url_params['after'] = after
        if limit is not None:
            url_params['limit'] = limit

        url = self.current_user_url / 'guilds' % url_params
        resp = await self._http.get(url)
        return [PartialUserGuild(**guild) for guild in resp.body]

    async def get_current_user_guild_member(self, guild_id: LikeSnowflake) -> Member:
        """Get the current user's guild member.

        Requires the guilds.members.read OAuth2 scope.

        Reference: https://discord.com/developers/docs/resources/user#get-current-user-guild-member

        Arguments:
            guild_id (LikeSnowflake): The ID of the guild.
        """
        url = self.current_user_url / f'guilds/{guild_id}/member'
        resp = await self._http.get(url)
        return Member(**resp.body)

    async def leave_guild(self, guild_id: LikeSnowflake):
        """Leave a guild.

        Reference: https://discord.com/developers/docs/resources/user#leave-guild

        Arguments:
            guild_id (LikeSnowflake): The ID of the guild to leave.
        """
        url = self.current_user_url / f'guilds/{guild_id}'
        await self._http.delete(url)

    async def create_dm(self, user_id: LikeSnowflake) -> Channel:
        """Create a DM with a user.

        Reference: https://discord.com/developers/docs/resources/user#create-dm

        Arguments:
            user_id (LikeSnowflake): The ID of the user to create a DM with.
        """
        url = self.current_user_url / 'channels'
        payload = {'recipient_id': user_id}
        resp = await self._http.post(url, payload)
        return Channel(**resp.body)

    async def create_group_dm(self, user_ids: list[LikeSnowflake]) -> Response:
        """Create a group DM.

        This endpoint was intended to be used with the now-deprecated GameBridge SDK.
        DMs created with this endpoint will not be shown in the Discord client.

        Reference: https://discord.com/developers/docs/resources/user#create-group-dm

        Arguments:
            user_ids (list[LikeSnowflake]): The IDs of the users to create a group DM with.
                The maximum number of users is 10.

        Raises:
            ValueError: If the number of users is greater than 10.
        """
        if len(user_ids) > 10:
            # limited by discord to 10 users per group DM
            raise ValueError('Cannot create a group DM with more than 10 users.')
        url = self.current_user_url / 'channels'
        payload = {'recipient_ids': user_ids}
        return await self._http.post(url, payload)
