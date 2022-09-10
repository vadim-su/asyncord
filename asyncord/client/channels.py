from __future__ import annotations

from asyncord.urls import REST_API_URL
from asyncord.typedefs import LikeSnowflake
from asyncord.client.resources import ClientSubresources
from asyncord.client.models.channels import Channel


class ChannelResource(ClientSubresources):
    users_url = REST_API_URL / 'channels'

    async def get_channel(self, channel_id: LikeSnowflake) -> Channel:
        """Get a channel by ID.

        Arguments:
            channel_id (LikeSnowflake): The ID of the channel.

        Returns:
            Channel: The channel object.
        """
        resp = await self._http.get(self.users_url / str(channel_id))
        return Channel(**resp.body)
