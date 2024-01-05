"""Channel Resource Endpoints.

These endpoints are for managing channels. Classic CRUD operations and related
endpoints like message creation.
"""
from __future__ import annotations

from asyncord.client.channels.models.channel_create import CreateChannelInputType
from asyncord.client.channels.models.channel_update import UpdateChannelInputType
from asyncord.client.channels.models.output import ChannelOutput
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.messages.resources import MessageResource
from asyncord.client.resources import ClientSubresource
from asyncord.snowflake import SnowflakeInput
from asyncord.typedefs import LikeSnowflake
from asyncord.urls import REST_API_URL


class ChannelResource(ClientSubresource):
    """Channel Resource Endpoints.

    These endpoints are for managing channels. If you want to create a channel,
    use the Guild Resource endpoints.

    More info at: https://discord.com/developers/docs/resources/channel
    """

    channels_url = REST_API_URL / 'channels'

    def messages(self, channel_id: LikeSnowflake) -> MessageResource:
        """Get the message resource for the channel.

        Args:
            channel_id: Channel id.

        Returns:
            Resource for managing messages.
        """
        return MessageResource(self, channel_id)

    async def get(self, channel_id: LikeSnowflake) -> ChannelOutput:
        """Get a channel by id.

        Args:
            channel_id: Channel id.

        Returns:
            Channel object.
        """
        url = self.channels_url / str(channel_id)
        resp = await self._http_client.get(url)
        return ChannelOutput(**resp.body)

    async def create_channel(
        self,
        guild_id: LikeSnowflake,
        channel_data: CreateChannelInputType,
        reason: str | None = None,
    ) -> ChannelOutput:
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

        channel_data.type = channel_data.type  # type: ignore

        payload = channel_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.post(url, payload, headers=headers)
        return ChannelOutput(**resp.body)

    async def update(
        self,
        channel_id: SnowflakeInput,
        channel_data: UpdateChannelInputType,
        reason: str | None = None,
    ) -> ChannelOutput:
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
        return ChannelOutput.model_validate(resp.body)

    async def delete(self, channel_id: LikeSnowflake, reason: str | None = None) -> None:
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
