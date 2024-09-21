from collections.abc import AsyncIterator

import pytest

from asyncord.client.channels.resources import ChannelResource
from asyncord.client.guilds.models.responses import InviteResponse
from asyncord.client.invites.resources import InvitesResource
from asyncord.client.scheduled_events.models.responses import ScheduledEventResponse
from tests.conftest import IntegrationTestData


@pytest.fixture
async def invite(
    channel_res: ChannelResource,
    invite_res: InvitesResource,
    integration_data: IntegrationTestData,
) -> AsyncIterator[InviteResponse]:
    """Create a channel invite and delete it after the test."""
    invite = await channel_res.create_channel_invite(integration_data.channel_id)
    yield invite
    await invite_res.delete_invite(invite.code)


async def test_get_invite(
    invite: InviteResponse,
    invite_res: InvitesResource,
) -> None:
    """Test getting an invite."""
    invite_response = await invite_res.get_invite(invite.code)
    assert invite_response.code == invite.code
    assert str(invite_response.url).endswith(invite.code)


async def test_get_invite_for_event(
    event: ScheduledEventResponse,
    invite: InviteResponse,
    invite_res: InvitesResource,
) -> None:
    """Test getting an invite for a guild scheduled event."""
    invite_response = await invite_res.get_invite(invite.code, guild_scheduled_event_id=event.id)
    assert invite_response.code == invite.code
    assert invite_response.guild_scheduled_event
    assert invite_response.guild_scheduled_event.id == event.id


async def test_get_invite_with_expiration(
    invite: InviteResponse,
    invite_res: InvitesResource,
) -> None:
    """Test getting an invite with expiration."""
    invite_response = await invite_res.get_invite(invite.code, with_expiration=True)
    assert invite_response.code == invite.code
    assert invite_response.expires_at


async def test_get_invite_with_counts(
    invite: InviteResponse,
    invite_res: InvitesResource,
) -> None:
    """Test getting an invite with counts."""
    invite_response = await invite_res.get_invite(invite.code, with_counts=True)
    assert invite_response.code == invite.code
    assert invite_response.approximate_presence_count
    assert invite_response.approximate_member_count
