from pathlib import Path

import pytest

from asyncord.client.users.models.requests import UpdateUserRequest
from asyncord.client.users.resources import UserResource
from tests.conftest import IntegrationTestData


async def test_get_current_user(users_res: UserResource) -> None:
    """Test getting the current user."""
    user = await users_res.get_current_user()
    assert user.id


async def test_get_user(users_res: UserResource) -> None:
    """Test getting a user."""
    current_user = await users_res.get_current_user()
    user = await users_res.get_user(current_user.id)
    assert user.id == current_user.id


@pytest.mark.limited()
async def test_update_current_user(users_res: UserResource) -> None:
    """Test updating the current user."""
    with Path('tests/data/test_avatar.png').open('rb') as f:
        avatar_data = f.read()

    with Path('tests/data/test_banner.gif').open('rb') as f:
        banner_data = f.read()

    user_data = UpdateUserRequest(
        username='Cucaryamba',
        avatar=avatar_data,
        banner=banner_data,
    )
    assert await users_res.update_user(user_data)


async def test_get_guilds(users_res: UserResource) -> None:
    """Test getting the current user's guilds."""
    guilds = await users_res.get_guilds()
    assert len(guilds)
    assert guilds[0].id


@pytest.mark.skip(reason='Skip the test because bots cannot use this endpoint')
async def test_get_current_user_guild_member(
    users_res: UserResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test geting the current user guild member."""
    member = await users_res.get_current_user_guild_member(integration_data.guild_id)
    assert member.user
    assert member.user.id


async def test_create_dm(
    users_res: UserResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test creating a DM channel with a user."""
    channel = await users_res.create_dm(integration_data.user_id)
    recipients = channel.recipients
    assert recipients
    assert len(recipients)
    assert integration_data.user_id in {recipient.id for recipient in recipients}
