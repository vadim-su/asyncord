from __future__ import annotations

import pytest

from asyncord.client.rest import RestClient
from asyncord.client.channels import ChannelResource
from asyncord.client.models.channels import ChannelType

TEST_GUILD_ID = '763522265874694144'
TEST_CHANNEL_ID = '920187645265608714'
TEST_MEMBER_ID = '934564225769148436'
TEST_ROLE_ID = '1010835042957787181'


class TestChannels:
    @pytest.fixture()
    async def channels(self, client: RestClient):
        return client.channels

    async def test_get_channel(self, channels: ChannelResource):
        channel = await channels.get(TEST_CHANNEL_ID)
        assert channel.id == TEST_CHANNEL_ID
        assert channel.guild_id == TEST_GUILD_ID
        assert channel.type is ChannelType.GUILD_TEXT
