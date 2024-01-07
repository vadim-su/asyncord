import pytest

from asyncord.client.channels.models.channel_create import (
    CreateAnoncementChannelInput,
    CreateCategoryChannelInput,
    CreateChannelInputType,
    CreateForumChannelInput,
    CreateMediaChannelInput,
    CreateStageChannelInput,
    CreateTextChannelInput,
    CreateVoiceChannelInput,
)
from asyncord.client.channels.models.channel_update import UpdateTextChannelInput
from asyncord.client.channels.models.common import ChannelType
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.http.errors import ClientError
from tests.conftest import IntegrationTestData

CHANNEL_NAME = 'test'

skip_server_unsupported = pytest.mark.skip(
    reason='This feature is not supported on the test server',
)


@pytest.mark.parametrize('channel_input', [
    pytest.param(CreateCategoryChannelInput(name=CHANNEL_NAME), id='test_create_category_channel'),
    pytest.param(CreateTextChannelInput(name=CHANNEL_NAME), id='test_create_text_channel'),  # type: ignore
    pytest.param(
        CreateAnoncementChannelInput(name=CHANNEL_NAME),  # type: ignore
        marks=skip_server_unsupported,
        id='test_create_announcement_channel',
    ),
    pytest.param(
        CreateForumChannelInput(name=CHANNEL_NAME),  # type: ignore
        marks=skip_server_unsupported,
        id='test_create_forum_channel',
    ),
    pytest.param(
        CreateMediaChannelInput(name=CHANNEL_NAME),  # type: ignore
        marks=skip_server_unsupported,
        id='test_create_media_channel',
    ),
    pytest.param(CreateVoiceChannelInput(name=CHANNEL_NAME), id='test_create_voice_channel'),  # type: ignore
    pytest.param(
        CreateStageChannelInput(name=CHANNEL_NAME),  # type: ignore
        marks=skip_server_unsupported,
        id='test_create_stage_channel',
    ),
])
async def test_create_and_delete_channel(channel_input: CreateChannelInputType, channels_res: ChannelResource, integration_data: IntegrationTestData):
    channel = await channels_res.create_channel(
        integration_data.guild_id, channel_input,
    )
    assert channel.guild_id == integration_data.guild_id
    assert channel.name == CHANNEL_NAME

    await channels_res.delete(channel.id)
    with pytest.raises(ClientError, match='Unknown Channel'):
        await channels_res.get(channel.id)


async def test_create_subchannel(
    channels_res: ChannelResource,
    integration_data: IntegrationTestData,
):
    category = await channels_res.create_channel(
        integration_data.guild_id,
        CreateCategoryChannelInput(
            name="test category",
            position=999,
        ),
    )

    text_chan = await channels_res.create_channel(
        integration_data.guild_id,
        channel_data=CreateTextChannelInput(
            name="test text subchannel",
            parent_id=category.id,
            rate_limit_per_user=2,
        ),  # type: ignore
    )
    voice_chan = await channels_res.create_channel(
        integration_data.guild_id,
        channel_data=CreateVoiceChannelInput(
            name="test voice subchannel",
            parent_id=category.id,
            bitrate=96000,
        ),  # type: ignore
    )

    # Delete channels
    for channel_id in {text_chan.id, voice_chan.id, category.id}:
        await channels_res.delete(channel_id)


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
        UpdateTextChannelInput(name='test'),  # type: ignore
    )
    assert channel.id == integration_data.channel_id
    assert channel.name == 'test'

    channel = await channels_res.update(
        integration_data.channel_id,
        UpdateTextChannelInput(name=preserved_name),  # type: ignore
    )
    assert channel.name == preserved_name
