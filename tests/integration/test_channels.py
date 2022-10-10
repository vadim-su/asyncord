from __future__ import annotations

import pytest

from asyncord.client.rest import RestClient
from asyncord.client.channels import ChannelResource
from asyncord.client.client_errors import ClientError
from asyncord.client.models.channels import ChannelType
from asyncord.client.models.channel_data import CreateChannelData, UpdateTextChannelData

TEST_GUILD_ID = '763522265874694144'
TEST_CHANNEL_ID = '920187645265608714'
TEST_MEMBER_ID = '934564225769148436'
TEST_ROLE_ID = '1010835042957787181'
TEST_MESSAGE_ID = '923584607427899402'


class TestChannels:
    @pytest.fixture()
    async def channels(self, client: RestClient):
        return client.channels

    async def test_create_and_delete_channel(self, channels: ChannelResource):
        channel = await channels.create_channel(
            TEST_GUILD_ID,
            CreateChannelData(
                name='test',
                type=ChannelType.GUILD_TEXT,
            ),
        )
        assert channel.guild_id == TEST_GUILD_ID
        assert channel.name == 'test'

        await channels.delete(channel.id)
        with pytest.raises(ClientError, match='Unknown Channel'):
            await channels.get(channel.id)

    async def test_get_channel(self, channels: ChannelResource):
        channel = await channels.get(TEST_CHANNEL_ID)
        assert channel.id == TEST_CHANNEL_ID
        assert channel.guild_id == TEST_GUILD_ID
        assert channel.type is ChannelType.GUILD_TEXT

    @pytest.mark.limited
    async def test_update_channel(self, channels: ChannelResource):
        preserved_name = (await channels.get(TEST_CHANNEL_ID)).name
        channel = await channels.update(TEST_CHANNEL_ID, UpdateTextChannelData(name='test'))
        assert channel.id == TEST_CHANNEL_ID
        assert channel.name == 'test'

        channel = await channels.update(TEST_CHANNEL_ID, UpdateTextChannelData(name=preserved_name))
        assert channel.name == preserved_name
