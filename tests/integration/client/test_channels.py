import pytest

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.channels.models.requests.creation import (
    CreateAnoncementChannelRequest,
    CreateCategoryChannelRequest,
    CreateChannelRequestType,
    CreateForumChannelRequest,
    CreateMediaChannelRequest,
    CreateStageChannelRequest,
    CreateTextChannelRequest,
    CreateVoiceChannelRequest,
)
from asyncord.client.channels.models.requests.updating import UpdateChannelPositionRequest, UpdateTextChannelRequest
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.http.errors import ClientError
from tests.conftest import IntegrationTestData

CHANNEL_NAME = 'test'

skip_server_unsupported = pytest.mark.skip(
    reason='This feature is not supported on the test server',
)


@pytest.mark.parametrize(
    'channel_input',
    [
        pytest.param(
            CreateCategoryChannelRequest(name=CHANNEL_NAME),
            id='test_create_category_channel',
        ),
        pytest.param(
            CreateTextChannelRequest(name=CHANNEL_NAME),
            id='test_create_text_channel',
        ),  # type: ignore
        pytest.param(
            CreateAnoncementChannelRequest(name=CHANNEL_NAME),  # type: ignore
            id='test_create_announcement_channel',
        ),
        pytest.param(
            CreateForumChannelRequest(name=CHANNEL_NAME),
            id='test_create_forum_channel',
        ),  # type: ignore
        pytest.param(
            CreateMediaChannelRequest(name=CHANNEL_NAME),  # type: ignore
            marks=skip_server_unsupported,
            id='test_create_media_channel',
        ),
        pytest.param(
            CreateVoiceChannelRequest(name=CHANNEL_NAME),
            id='test_create_voice_channel',
        ),  # type: ignore
        pytest.param(
            CreateStageChannelRequest(name=CHANNEL_NAME),
            id='test_create_stage_channel',
        ),  # type: ignore
    ],
)
async def test_create_and_delete_channel(
    channel_input: CreateChannelRequestType,
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test creating and deleting channels."""
    channel = await channel_res.create_channel(integration_data.guild_id, channel_input)
    assert channel.guild_id == integration_data.guild_id
    assert channel.name == CHANNEL_NAME

    await channel_res.delete(channel.id)
    with pytest.raises(ClientError, match='Unknown Channel'):
        await channel_res.get(channel.id)


async def test_create_subchannel(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test creating and deleting subchannels."""
    category = await channel_res.create_channel(
        integration_data.guild_id,
        CreateCategoryChannelRequest(
            name='test category',
            position=999,
        ),
    )

    text_chan = await channel_res.create_channel(
        integration_data.guild_id,
        channel_data=CreateTextChannelRequest(
            name='test text subchannel',
            parent_id=category.id,
            rate_limit_per_user=2,
        ),  # type: ignore
    )
    voice_chan = await channel_res.create_channel(
        integration_data.guild_id,
        channel_data=CreateVoiceChannelRequest(
            name='test voice subchannel',
            parent_id=category.id,
            bitrate=96000,
        ),  # type: ignore
    )

    # Delete channels
    for channel_id in {text_chan.id, voice_chan.id, category.id}:
        await channel_res.delete(channel_id)


async def test_get_channel(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting a channel."""
    channel = await channel_res.get(integration_data.channel_id)
    assert channel.id == integration_data.channel_id
    assert channel.guild_id == integration_data.guild_id
    assert channel.type is ChannelType.GUILD_TEXT


async def test_create_channel_invite(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test creating channel invite."""
    invite = await channel_res.create_channel_invite(integration_data.channel_id)
    assert invite.code


async def test_get_channel_invites(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting channel invites."""
    invites = await channel_res.get_channel_invites(integration_data.channel_id)
    assert isinstance(invites, list)


async def test_trigger_typping_indicator(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test trigger typing indicator."""
    await channel_res.trigger_typing_indicator(integration_data.channel_id)


@pytest.mark.limited()
async def test_update_channel_position(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test updating channel position."""
    channel = await channel_res.get(integration_data.channel_id)
    position = channel.position

    await channel_res.update_channel_position(
        integration_data.guild_id,
        [
            UpdateChannelPositionRequest(
                id=integration_data.channel_id,
                position=channel.position + 1,
            ),
        ],
    )

    updated_channel = await channel_res.get(integration_data.channel_id)

    assert channel.position == updated_channel.position - 1

    await channel_res.update_channel_position(
        integration_data.guild_id,
        [
            UpdateChannelPositionRequest(
                id=integration_data.channel_id,
                position=position,
            ),
        ],
    )


@pytest.mark.limited()
async def test_update_channel(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test updating a channel."""
    preserved_name = (await channel_res.get(integration_data.channel_id)).name

    channel = await channel_res.update(
        integration_data.channel_id,
        UpdateTextChannelRequest(name='test'),  # type: ignore
    )
    assert channel.id == integration_data.channel_id
    assert channel.name == 'test'

    channel = await channel_res.update(
        integration_data.channel_id,
        UpdateTextChannelRequest(name=preserved_name),  # type: ignore
    )
    assert channel.name == preserved_name
