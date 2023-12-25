import pytest

from asyncord.client.channels import ChannelResource
from asyncord.client.http.errors import ClientError
from asyncord.client.models.channel_data import CreateChannelData, UpdateTextChannelData
from asyncord.client.models.channels import ChannelType
from tests.conftest import IntegrationTestData


async def test_create_and_delete_channel(channels_res: ChannelResource, integration_data: IntegrationTestData):
    channel = await channels_res.create_channel(
        integration_data.guild_id,
        CreateChannelData(
            name='test',
            type=ChannelType.GUILD_TEXT,
        ),
    )
    assert channel.guild_id == integration_data.guild_id
    assert channel.name == 'test'

    await channels_res.delete(channel.id)
    with pytest.raises(ClientError, match='Unknown Channel'):
        await channels_res.get(channel.id)


async def test_get_channel(channels_res: ChannelResource, integration_data: IntegrationTestData):
    channel = await channels_res.get(integration_data.channel_id)
    assert channel.id == integration_data.channel_id
    assert channel.guild_id == integration_data.guild_id
    assert channel.type is ChannelType.GUILD_TEXT


@pytest.mark.limited
async def test_update_channel(channels_res: ChannelResource, integration_data: IntegrationTestData):
    preserved_name = (await channels_res.get(integration_data.channel_id)).name

    channel = await channels_res.update(
        integration_data.channel_id,
        UpdateTextChannelData(name='test')
    )
    assert channel.id == integration_data.channel_id
    assert channel.name == 'test'

    channel = await channels_res.update(
        integration_data.channel_id,
        UpdateTextChannelData(name=preserved_name)
    )
    assert channel.name == preserved_name
