"""Channel Resource Endpoints.

These endpoints are for managing channels. Classic CRUD operations and related
endpoints like message creation.
"""

from __future__ import annotations

from asyncord.client.channels.models.requests.creation import ChannelInviteRequest, CreateChannelRequestType
from asyncord.client.channels.models.requests.updating import (
    UpdateChannelPermissionsRequest,
    UpdateChannelRequestType,
)
from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.guilds.models.responses import InviteResponse
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.messages.resources import MessageResource
from asyncord.client.resources import ClientSubresource
from asyncord.client.threads.resources import ThreadResource
from asyncord.snowflake import SnowflakeInputType
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL


class ChannelResource(ClientSubresource):
    """Channel Resource Endpoints.

    These endpoints are for managing channels. If you want to create a channel,
    use the Guild Resource endpoints.

    More info at: https://discord.com/developers/docs/resources/channel
    """

    channels_url = REST_API_URL / 'channels'

    def messages(self, channel_id: SnowflakeInputType) -> MessageResource:
        """Get the message resource for the channel.

        Args:
            channel_id: Channel id.

        Returns:
            Resource for managing messages.
        """
        return MessageResource(self, channel_id)

    def threads(self, channel_id: SnowflakeInputType) -> ThreadResource:
        """Get the thread resource for the channel.

        Args:
            channel_id: Channel id.

        Returns:
            Resource for managing threads.
        """
        return ThreadResource(self, channel_id)

    async def get(self, channel_id: SnowflakeInputType) -> ChannelResponse:
        """Get a channel by id.

        Args:
            channel_id: Channel id.

        Returns:
            Channel object.
        """
        url = self.channels_url / str(channel_id)
        resp = await self._http_client.get(url)
        return ChannelResponse(**resp.body)

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

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        # We want to send this field to the api, but exclude_unset will remove it
        # if it's not set (or Default). So we set it to itself to make sure it's set.
        channel_data.type = channel_data.type  # type: ignore

        payload = channel_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url, payload, headers=headers)
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

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = channel_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.patch(url, payload, headers=headers)
        return ChannelResponse.model_validate(resp.body)

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

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url, headers=headers)

    async def update_permissions(
        self,
        channel_id: SnowflakeInputType,
        overwrite_id: SnowflakeInputType,
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
            overwrite_id: Role or user id.
            permission_data: The data to update the permissions with.
            reason: Reason for updating the permissions.
        """
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = permission_data.model_dump(mode='json', exclude_unset=True)

        url = self.channels_url / str(channel_id) / 'permissions' / str(overwrite_id)

        await self._http_client.put(
            url,
            payload,
            headers=headers,
        )

    async def delete_permission(
        self,
        channel_id: SnowflakeInputType,
        overwrite_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Delete a channel permission overwrite for a user or role in a channel.

        Args:
            channel_id: Channel id.
            overwrite_id: Role or user id.
            reason: Reason for deleting the permission.
        """
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        url = self.channels_url / str(channel_id) / 'permissions' / str(overwrite_id)

        await self._http_client.delete(url, headers=headers)

    async def get_channel_invites(
        self,
        channel_id: SnowflakeInputType,
    ) -> list[InviteResponse]:
        """Get the invites for a channel.

        Reference:
        https://canary.discord.com/developers/docs/resources/channel#get-channel-invites

        Args:
            channel_id: Channel id.

        Returns:
            List of invites for the channel.
        """
        url = self.channels_url / str(channel_id) / 'invites'
        resp = await self._http_client.get(url)
        return list_model(InviteResponse).validate_python(resp.body)

    async def create_channel_invite(
        self,
        channel_id: SnowflakeInputType,
        invite_request: ChannelInviteRequest | None = None,
    ) -> InviteResponse:
        """Create a new invite for a channel.

        Reference:
        https://canary.discord.com/developers/docs/resources/channel#create-channel-invite

        Args:
            channel_id: Channel id.
            invite_request: Data for creating the invite.

        Returns:
            Created invite.
        """
        url = self.channels_url / str(channel_id) / 'invites'

        payload = {}

        if invite_request:
            payload = invite_request.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.post(url, payload)
        return InviteResponse.model_validate(resp.body)

    # TODO: Add webhook models once they are implemented.
    async def follow_announcement_channel(
        self,
        channel_id: SnowflakeInputType,
        webhook_channel_id: SnowflakeInputType,
    ) -> dict:
        """Follow an Announcement channel to send messages to a target channel.

        Reference:
        https://canary.discord.com/developers/docs/resources/channel#follow-announcement-channel
        """
        url = self.channels_url / str(channel_id) / 'followers'

        payload = {
            'webhook_channel_id': str(webhook_channel_id),
        }

        resp = await self._http_client.post(url, payload)
        return resp.body

    async def trigger_typing_indicator(
        self,
        channel_id: SnowflakeInputType,
    ) -> None:
        """Post a typing indicator for the specified channel.

        Expires after 10 seconds.

        Reference:
        https://canary.discord.com/developers/docs/resources/channel#trigger-typing-indicator
        """
        url = self.channels_url / str(channel_id) / 'typing'

        payload = {}

        await self._http_client.post(url, payload)
