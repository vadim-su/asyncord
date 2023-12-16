from __future__ import annotations

import pytest

from asyncord.client.channels import ChannelResource
from asyncord.client.http.errors import ClientError
from asyncord.client.models.channel_data import CreateChannelData, UpdateTextChannelData
from asyncord.client.models.channels import ChannelType
from asyncord.client.rest import RestClient
from tests.conftest import IntegrationData


class TestChannels:
    @pytest.fixture()
    async def channels(self, client: RestClient):
        return client.channels

    async def test_create_and_delete_channel(
        self,
        channels: ChannelResource,
        integration_data: IntegrationData
    ):
        channel = await channels.create_channel(
            integration_data.TEST_GUILD_ID,
            CreateChannelData(
                name='test',
                type=ChannelType.GUILD_TEXT,
            ),
        )
        assert channel.guild_id == integration_data.TEST_GUILD_ID
        assert channel.name == 'test'

        await channels.delete(channel.id)
        with pytest.raises(ClientError, match='Unknown Channel'):
            await channels.get(channel.id)

    async def test_get_channel(
        self,
        channels: ChannelResource,
        integration_data: IntegrationData
    ):
        channel = await channels.get(integration_data.TEST_CHANNEL_ID)
        assert channel.id == integration_data.TEST_CHANNEL_ID
        assert channel.guild_id == integration_data.TEST_GUILD_ID
        assert channel.type is ChannelType.GUILD_TEXT

    @pytest.mark.limited
    async def test_update_channel(
        self,
        channels: ChannelResource,
        integration_data: IntegrationData
    ):
        preserved_name = (await channels.get(integration_data.TEST_CHANNEL_ID)).name

        channel = await channels.update(
            integration_data.TEST_CHANNEL_ID,
            UpdateTextChannelData(name='test')
        )
        assert channel.id == integration_data.TEST_CHANNEL_ID
        assert channel.name == 'test'

        channel = await channels.update(
            integration_data.TEST_CHANNEL_ID,
            UpdateTextChannelData(name=preserved_name)
        )
        assert channel.name == preserved_name
