from collections.abc import AsyncGenerator

import pytest

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.channels.models.requests.creation import (
    ChannelInviteRequest,
    CreateAnoncementChannelRequest,
    CreateCategoryChannelRequest,
    CreateChannelRequestType,
    CreateForumChannelRequest,
    CreateMediaChannelRequest,
    CreateStageChannelRequest,
    CreateTextChannelRequest,
    CreateVoiceChannelRequest,
)
from asyncord.client.channels.models.requests.updating import (
    UpdateChannelPermissionsRequest,
    UpdateChannelPositionRequest,
    UpdateTextChannelRequest,
)
from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.models.permissions import PermissionFlag
from tests.conftest import IntegrationTestData

CHANNEL_NAME = 'test'

skip_server_unsupported = pytest.mark.skip(
    reason='This feature is not supported on the test server',
)


@pytest.fixture
async def channel(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> AsyncGenerator[ChannelResponse, None]:
    """Create a channel for testing."""
    channel = await channel_res.create_channel(
        guild_id=integration_data.guild_id,
        channel_data=CreateTextChannelRequest(name='test'),
    )

    yield channel

    await channel_res.delete(channel.id)


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
    text_chan_id = None
    voice_chan_id = None
    try:
        text_chan = await channel_res.create_channel(
            integration_data.guild_id,
            channel_data=CreateTextChannelRequest(
                name='test text subchannel',
                parent_id=category.id,
                rate_limit_per_user=2,
            ),  # type: ignore
        )
        text_chan_id = text_chan.id
        voice_chan = await channel_res.create_channel(
            integration_data.guild_id,
            channel_data=CreateVoiceChannelRequest(
                name='test voice subchannel',
                parent_id=category.id,
                bitrate=96000,
            ),  # type: ignore
        )
        voice_chan_id = voice_chan.id
        assert text_chan.parent_id == category.id
    finally:
        # Delete channels
        for channel_id in {text_chan_id, voice_chan_id, category.id}:
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


async def test_get_channel_invites(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting channel invites."""
    invites = await channel_res.get_channel_invites(integration_data.channel_id)
    assert isinstance(invites, list)


@pytest.mark.parametrize(
    'invite_data',
    [
        None,
        ChannelInviteRequest(max_age=60, max_uses=1),
    ],
)
async def test_create_channel_invite(
    invite_data: ChannelInviteRequest | None,
    stage_channel: ChannelResponse,
    channel_res: ChannelResource,
) -> None:
    """Test creating a channel invite."""
    invite = await channel_res.create_channel_invite(stage_channel.id, invite_data)
    assert invite.code


async def test_trigger_typping_indicator(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test trigger typing indicator."""
    await channel_res.trigger_typing_indicator(integration_data.channel_id)


async def test_update_channel_position(
    stage_channel: ChannelResponse,
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test updating channel position."""
    await channel_res.update_channel_position(
        integration_data.guild_id,
        [
            UpdateChannelPositionRequest(
                id=stage_channel.id,
                position=stage_channel.position + 1,  # type: ignore
            ),
        ],
    )

    updated_channel = await channel_res.get(stage_channel.id)
    assert updated_channel.position == stage_channel.position + 1  # type: ignore


async def test_update_channel(
    stage_channel: ChannelResponse,
    channel_res: ChannelResource,
) -> None:
    """Test updating a channel."""
    assert stage_channel.name != 'test'

    channel = await channel_res.update(
        stage_channel.id,
        UpdateTextChannelRequest(name='test'),  # type: ignore
    )

    assert channel.name == 'test'


async def test_permissions_lifecycle(
    stage_channel: ChannelResponse,
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test full lifecycle of channel permissions."""
    allowed_permissions = PermissionFlag.VIEW_AUDIT_LOG | PermissionFlag.SEND_MESSAGES
    await channel_res.update_permissions(
        channel_id=stage_channel.id,
        role_or_user_id=integration_data.role_id,
        permission_data=UpdateChannelPermissionsRequest(
            type='role',
            allow=allowed_permissions,
            deny=PermissionFlag.USE_APPLICATION_COMMANDS,
        ),
    )

    update_channel = await channel_res.get(stage_channel.id)
    assert update_channel.permission_overwrites
    assert update_channel.permission_overwrites[0].allow == allowed_permissions

    await channel_res.delete_permission(
        channel_id=stage_channel.id,
        role_or_user_id=integration_data.role_id,
    )

    update_channel = await channel_res.get(stage_channel.id)
    assert not update_channel.permission_overwrites


async def test_follow_announcement_channel(
    announcement_channel: ChannelResponse,
    channel: ChannelResponse,
    channel_res: ChannelResource,
) -> None:
    """Test following an announcement channel."""
    followed_chan_resp = await channel_res.follow_announcement_channel(
        channel_id=announcement_channel.id,
        target_channel_id=channel.id,
    )
    assert followed_chan_resp.webhook_id
    assert followed_chan_resp.channel_id == announcement_channel.id
