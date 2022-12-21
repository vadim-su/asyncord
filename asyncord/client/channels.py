"""Channel Resource Endpoints.

These endpoints are for managing channels. Classic CRUD operations and related
endpoints like message creation.
"""
from __future__ import annotations

from asyncord.urls import REST_API_URL
from asyncord.typedefs import LikeSnowflake
from asyncord.client.headers import AUDIT_LOG_REASON
from asyncord.client.messages import MessageResource
from asyncord.client.resources import ClientSubresources
from asyncord.client.models.channels import Channel
from asyncord.client.models.channel_data import CreateChannelData, UpdateChannelDataType


class ChannelResource(ClientSubresources):
    """Channel Resource Endpoints.

    These endpoints are for managing channels. If you want to create a channel,
    use the Guild Resource endpoints.

    More info at: https://discord.com/developers/docs/resources/channel
    """

    channels_url = REST_API_URL / 'channels'

    def messages(self, channel_id: LikeSnowflake) -> MessageResource:
        """Get the message resource for the channel.

        Arguments:
            channel_id (LikeSnowflake): Channel id.

        Returns:
            MessageResource: Resource for managing messages.
        """
        return MessageResource(self, channel_id)

    async def get(self, channel_id: LikeSnowflake) -> Channel:
        """Get a channel by ID.

        Arguments:
            channel_id (LikeSnowflake): Channel id.

        Returns:
            Channel: Channel object.
        """
        url = self.channels_url / str(channel_id)
        resp = await self._http.get(url)
        return Channel(**resp.body)

    async def create_channel(
        self,
        guild_id: LikeSnowflake,
        channel_data: CreateChannelData,
        reason: str | None = None,
    ) -> Channel:
        """Create a new channel object for the guild.

        This endpoint can only be used on guilds.

        Arguments:
            guild_id (LikeSnowflake): Guild ID.
            channel_data (UpdateChannelDataType): Data to create the channel with.
            reason (str, optional): Reason for creating the channel.

        Returns:
            Channel: Created channel object.
        """
        url = REST_API_URL / 'guilds' / str(guild_id) / 'channels'

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = channel_data.dict(exclude_unset=True)

        resp = await self._http.post(url, payload, headers=headers)
        return Channel(**resp.body)

    async def update(
        self,
        channel_id: LikeSnowflake,
        channel_data: UpdateChannelDataType,
        reason: str | None = None,
    ) -> Channel:
        """Update a channel's settings.

        Arguments:
            channel_id (LikeSnowflake): Channel id.
            channel_data (UpdateChannelDataType): The data to update the channel with.
            reason (str, optional): The reason for updating the channel.

        Returns:
            Channel: Updated channel object.
        """
        url = self.channels_url / str(channel_id)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = channel_data.dict(exclude_unset=True)

        resp = await self._http.patch(url, payload, headers=headers)
        return Channel(**resp.body)

    async def delete(self, channel_id: LikeSnowflake, reason: str | None = None) -> None:
        """Delete a channel, or close a private message.

        Deleting a guild channel cannot be undone. Use this with caution,
        as it is impossible to undo this action when performed on a guild channel.
        In contrast, when used with a private message, it is possible to undo
        the action by opening a private message with the recipient again.

        For Community guilds, the Rules or Guidelines channel and
        the Community Updates channel cannot be deleted.

        Arguments:
            channel_id (LikeSnowflake): Channel id.
            reason (str, optional): Reason for deleting the channel.
        """
        url = self.channels_url / str(channel_id)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http.delete(url, headers=headers)
