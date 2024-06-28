"""This module contains the UserResource class, which is used to interact with."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.members.models.responses import MemberResponse
from asyncord.client.resources import APIResource
from asyncord.client.users.models.responses import (
    ApplicationRoleConnectionResponse,
    UserConnectionResponse,
    UserGuildResponse,
    UserResponse,
)
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.users.models.requests import (
        UpdateApplicationRoleConnectionRequest,
        UpdateUserRequest,
    )
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('UserResource',)


class UserResource(APIResource):
    """User resource.

    Attributes:
        users_url: Base users url.
        current_user_url: Current user url.
    """

    users_url = REST_API_URL / 'users'
    current_user_url = users_url / '@me'
    channels_url = REST_API_URL / 'channels'

    async def get_current_user(self) -> UserResponse:
        """Get the current user.

        Reference:
        https://discord.com/developers/docs/resources/user#modify-current-user
        """
        resp = await self._http_client.get(url=self.current_user_url)
        return UserResponse.model_validate(resp.body)

    async def get_user(self, user_id: SnowflakeInputType) -> UserResponse:
        """Get a user.

        Reference:
        https://discord.com/developers/docs/resources/user#modify-current-user

        Args:
            user_id: ID of the user to get.
        """
        url = self.users_url / str(user_id)
        resp = await self._http_client.get(url=url)
        return UserResponse.model_validate(resp.body)

    async def update_user(self, user_update_data: UpdateUserRequest) -> UserResponse:
        """Update the current user.

        Args:
            user_update_data: Update user request model.

        Reference:
        https://discord.com/developers/docs/resources/user#modify-current-user
        """
        payload = user_update_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(url=self.current_user_url, payload=payload)
        return UserResponse.model_validate(resp.body)

    async def get_guilds(
        self,
        before: SnowflakeInputType | None = None,
        after: SnowflakeInputType | None = None,
        limit: int | None = None,
    ) -> list[UserGuildResponse]:
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
        resp = await self._http_client.get(url=url)
        return list_model(UserGuildResponse).validate_python(resp.body)

    async def get_current_user_guild_member(self, guild_id: SnowflakeInputType) -> MemberResponse:
        """Get the current user's guild member.

        Requires the guilds.members.read OAuth2 scope.

        Reference:
        https://discord.com/developers/docs/resources/user#get-current-user-guild-member

        Args:
            guild_id: ID of the guild.
        """
        url = self.current_user_url / f'guilds/{guild_id}/member'
        resp = await self._http_client.get(url=url)
        return MemberResponse.model_validate(resp.body)

    async def leave_guild(self, guild_id: SnowflakeInputType) -> None:
        """Leave a guild.

        Reference:
        https://discord.com/developers/docs/resources/user#leave-guild

        Args:
            guild_id: ID of the guild to leave.
        """
        url = self.current_user_url / f'guilds/{guild_id}'
        await self._http_client.delete(url=url)

    async def create_dm(self, user_id: SnowflakeInputType) -> ChannelResponse:
        """Create a DM with a user.

        Reference:
        https://discord.com/developers/docs/resources/user#create-dm

        Args:
            user_id: ID of the user to create a DM with.
        """
        url = self.current_user_url / 'channels'
        payload = {'recipient_id': user_id}
        resp = await self._http_client.post(url=url, payload=payload)
        return ChannelResponse.model_validate(resp.body)

    async def create_group_dm(self, user_ids: Sequence[SnowflakeInputType]) -> ChannelResponse:
        """Create a group DM.

        This endpoint was intended to be used with the now-deprecated GameBridge SDK.
        DMs created with this endpoint will not be shown in the Discord client.

        Reference:
        https://discord.com/developers/docs/resources/user#create-group-dm

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
        resp = await self._http_client.post(url=url, payload=payload)
        return ChannelResponse.model_validate(resp.body)

    async def add_group_dm_recipient(
        self,
        channel_id: SnowflakeInputType,
        user_id: SnowflakeInputType,
        access_token: str,
        nick: str,
    ) -> None:
        """Adds a recipient to a Group DM.

        Args:
            channel_id: Channel ID of the Group DM.
            user_id: User ID to add.
            access_token: Access token of the user to add.
            nick: Nickname of the user to add.

        Reference:
        https://discord.com/developers/docs/resources/channel#group-dm-add-recipient
        """
        url = self.channels_url / str(channel_id) / 'recipients' / str(user_id)

        payload = {'access_token': access_token, 'nick': nick}

        await self._http_client.put(url=url, payload=payload)

    async def remove_group_dm_recipient(
        self,
        channel_id: SnowflakeInputType,
        user_id: SnowflakeInputType,
    ) -> None:
        """Removes a recipient from a Group DM.

        Reference:
        https://discord.com/developers/docs/resources/channel#group-dm-remove-recipient
        """
        url = self.channels_url / str(channel_id) / 'recipients' / str(user_id)

        await self._http_client.delete(url=url)

    async def get_current_user_connections(
        self,
    ) -> list[UserConnectionResponse]:
        """Returns a list of connection objects.

        Reference:
        https://discord.com/developers/docs/resources/user#get-current-user-connections
        """
        url = self.current_user_url / 'connections'
        resp = await self._http_client.get(url=url)
        return list_model(UserConnectionResponse).validate_python(resp.body)

    async def get_current_user_application_role_connection(  # pragma: no cover
        self,
        application_id: SnowflakeInputType,
    ) -> ApplicationRoleConnectionResponse:
        """Returns the connection object for the current user's application.

        This endpoint can not be used by bots.

        Reference:
        https://discord.com/developers/docs/resources/user#get-current-user-application-role-connection

        Args:
            application_id: ID of the application.
        """
        url = self.current_user_url / 'applications' / str(application_id) / 'role-connection'
        resp = await self._http_client.get(url=url)
        return ApplicationRoleConnectionResponse.model_validate(resp.body)

    async def update_current_user_application_role_connection(  # pragma: no cover
        self,
        application_id: SnowflakeInputType,
        update_data: UpdateApplicationRoleConnectionRequest,
    ) -> ApplicationRoleConnectionResponse:
        """Modify the current user's application role connection.

        This endpoint can not be used by bots.

        Reference:
        https://discord.com/developers/docs/resources/user#update-current-user-application-role-connection\

        Args:
            application_id: ID of the application.
            update_data: Update application role connection request model.
        """
        url = self.current_user_url / 'applications' / str(application_id) / 'role-connection'
        payload = update_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.put(url=url, payload=payload)
        return ApplicationRoleConnectionResponse.model_validate(resp.body)
