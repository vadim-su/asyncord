"""Channel Resource Endpoints.

These endpoints are for managing channels. Classic CRUD operations and related
endpoints like message creation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.channels.models.requests.updating import UpdateChannelPermissionsRequest
from asyncord.client.channels.models.responses import ChannelResponse, FollowedChannelResponse
from asyncord.client.guilds.models.responses import InviteResponse
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.messages.resources import MessageResource
from asyncord.client.polls.resources import PollsResource
from asyncord.client.resources import APIResource
from asyncord.client.threads.resources import ThreadResource
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.channels.models.requests.creation import (
        ChannelInviteRequest,
        CreateChannelRequestType,
    )
    from asyncord.client.channels.models.requests.updating import (
        UpdateChannelPositionRequest,
        UpdateChannelRequestType,
    )
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('ChannelResource',)


class ChannelResource(APIResource):
    """Channel Resource Endpoints.

    These endpoints are for managing channels. If you want to create a channel,
    use the Guild Resource endpoints.

    Reference:
    https://discord.com/developers/docs/resources/channel
    """

    channels_url = REST_API_URL / 'channels'

    def messages(self, channel_id: SnowflakeInputType) -> MessageResource:
        """Get the message resource for the channel.

        Args:
            channel_id: Channel id.

        Returns:
            Resource for managing messages.
        """
        return MessageResource(self._http_client, channel_id)

    def polls(self, channel_id: SnowflakeInputType) -> PollsResource:
        """Get the polls resource for the channel.

        Args:
            channel_id: Channel id.

        Returns:
            Resource for managing polls.
        """
        return PollsResource(self._http_client, channel_id)

    def threads(self, channel_id: SnowflakeInputType) -> ThreadResource:
        """Get the thread resource for the channel.

        Args:
            channel_id: Channel id.

        Returns:
            Resource for managing threads.
        """
        return ThreadResource(self._http_client, channel_id)

    async def get(self, channel_id: SnowflakeInputType) -> ChannelResponse:
        """Get a channel by id.

        Args:
            channel_id: Channel id.

        Returns:
            Channel object.
        """
        url = self.channels_url / str(channel_id)
        resp = await self._http_client.get(url=url)
        return ChannelResponse.model_validate(resp.body)

    async def create_channel(
        self,
        guild_id: SnowflakeInputType,
        channel_data: CreateChannelRequestType,
        reason: str | None = None,
    ) -> ChannelResponse:
        """Create a new channel object for the guild.

        This endpoint can only be used on guilds.

        Args:
            guild_id: Guild id.
            channel_data: Data to create the channel with.
            reason: Reason for creating the channel.

        Returns:
            Created channel object.
        """
        url = REST_API_URL / 'guilds' / str(guild_id) / 'channels'

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        # We want to send this field to the api, but exclude_unset will remove it
        # if it's not set (or Default). So we set it to itself to make sure it's set.
        channel_data.type = channel_data.type  # type: ignore

        payload = channel_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url=url, payload=payload, headers=headers)
        return ChannelResponse.model_validate(resp.body)

    async def update(
        self,
        channel_id: SnowflakeInputType,
        channel_data: UpdateChannelRequestType,
        reason: str | None = None,
    ) -> ChannelResponse:
        """Update a channel's settings.

        Args:
            channel_id: Channel id.
            channel_data: The data to update the channel with.
            reason: The reason for updating the channel.

        Returns:
            Updated channel object.
        """
        url = self.channels_url / str(channel_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = channel_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.patch(url=url, payload=payload, headers=headers)
        return ChannelResponse.model_validate(resp.body)

    async def update_channel_position(
        self,
        guild_id: SnowflakeInputType,
        position_data: list[UpdateChannelPositionRequest],
    ) -> None:
        """Update the positions of a set of channel objects.

        Reference:
        https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions

        Args:
            guild_id: Guild id.
            position_data: The data to update the channel positions with.
        """
        url = REST_API_URL / 'guilds' / str(guild_id) / 'channels'

        payload = [position.model_dump(mode='json', exclude_unset=True) for position in position_data]

        await self._http_client.patch(url=url, payload=payload)

    async def delete(self, channel_id: SnowflakeInputType, reason: str | None = None) -> None:
        """Delete a channel, or close a private message.

        Deleting a guild channel cannot be undone. Use this with caution,
        as it is impossible to undo this action when performed on a guild channel.
        In contrast, when used with a private message, it is possible to undo
        the action by opening a private message with the recipient again.

        For Community guilds, the Rules or Guidelines channel and
        the Community Updates channel cannot be deleted.

        Args:
            channel_id: Channel id.
            reason: Reason for deleting the channel.
        """
        url = self.channels_url / str(channel_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url=url, headers=headers)

    async def update_permissions(
        self,
        channel_id: SnowflakeInputType,
        role_or_user_id: SnowflakeInputType,
        permission_data: UpdateChannelPermissionsRequest,
        reason: str | None = None,
    ) -> None:
        """Edit the channel permission overwrites for a user or role in a channel.

        Only usable for guild channels. Requires the MANAGE_ROLES permission.
        Only permissions your bot has in the guild or parent channel (if applicable)
        can be allowed/denied (unless your bot has a MANAGE_ROLES overwrite in the channel).
        Returns a 204 empty response on success.

        Args:
            channel_id: Channel id.
            role_or_user_id: Role or user id.
            permission_data: The data to update the permissions with.
            reason: Reason for updating the permissions.
        """
        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = permission_data.model_dump(mode='json', exclude_unset=True)

        url = self.channels_url / str(channel_id) / 'permissions' / str(role_or_user_id)
        await self._http_client.put(
            url=url,
            payload=payload,
            headers=headers,
        )

    async def delete_permission(
        self,
        channel_id: SnowflakeInputType,
        role_or_user_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Delete a channel permission overwrite for a user or role in a channel.

        Args:
            channel_id: Channel id.
            role_or_user_id: Role or user id.
            reason: Reason for deleting the permission.
        """
        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        url = self.channels_url / str(channel_id) / 'permissions' / str(role_or_user_id)

        await self._http_client.delete(url=url, headers=headers)

    async def get_channel_invites(self, channel_id: SnowflakeInputType) -> list[InviteResponse]:
        """Get the invites for a channel.

        Reference:
        https://discord.com/developers/docs/resources/channel#get-channel-invites

        Args:
            channel_id: Channel id.

        Returns:
            List of invites for the channel.
        """
        url = self.channels_url / str(channel_id) / 'invites'
        resp = await self._http_client.get(url=url)
        return list_model(InviteResponse).validate_python(resp.body)

    async def create_channel_invite(
        self,
        channel_id: SnowflakeInputType,
        invite_data: ChannelInviteRequest | None = None,
        reason: str | None = None,
    ) -> InviteResponse:
        """Create a new invite for a channel.

        Reference:
        https://discord.com/developers/docs/resources/channel#create-channel-invite

        Args:
            channel_id: Channel id.
            invite_data: Data for creating the invite. Default is None.
                If None, a default invite will be created.
            reason: Reason for creating the invite.

        Returns:
            Created invite.
        """
        url = self.channels_url / str(channel_id) / 'invites'

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = {}

        if invite_data:
            payload = invite_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.post(url=url, payload=payload, headers=headers)
        return InviteResponse.model_validate(resp.body)

    async def follow_announcement_channel(
        self,
        channel_id: SnowflakeInputType,
        target_channel_id: SnowflakeInputType,
    ) -> FollowedChannelResponse:
        """Follow an Announcement channel to send messages to a target channel.

        Args:
            channel_id: Channel id.
            target_channel_id: Channel id to send messages to.

        Reference:
        https://discord.com/developers/docs/resources/channel#follow-announcement-channel
        """
        url = self.channels_url / str(channel_id) / 'followers'

        payload = {
            'webhook_channel_id': str(target_channel_id),
        }

        resp = await self._http_client.post(url=url, payload=payload)
        return FollowedChannelResponse.model_validate(resp.body)

    async def trigger_typing_indicator(self, channel_id: SnowflakeInputType) -> None:
        """Post a typing indicator for the specified channel.

        Expires after 10 seconds.

        Reference:
        https://discord.com/developers/docs/resources/channel#trigger-typing-indicator
        """
        url = self.channels_url / str(channel_id) / 'typing'

        payload = {}

        await self._http_client.post(url=url, payload=payload)
