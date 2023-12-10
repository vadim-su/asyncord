from __future__ import annotations

import os

import pytest

from asyncord.client.channels import ChannelResource
from asyncord.client.http.errors import ClientError
from asyncord.client.models.channel_data import CreateChannelData, UpdateTextChannelData
from asyncord.client.models.channels import ChannelType
from asyncord.client.rest import RestClient

TEST_GUILD_ID = os.environ.get('TEST_GUILD_ID')
TEST_CHANNEL_ID = os.environ.get('TEST_CHANNEL_ID')
TEST_MEMBER_ID = os.environ.get('TEST_MEMBER_ID')
TEST_ROLE_ID = os.environ.get('TEST_ROLE_ID')
TEST_MESSAGE_ID = os.environ.get('TEST_MESSAGE_ID')


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
