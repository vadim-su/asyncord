from pathlib import Path
from typing import Literal

import pytest

from asyncord.client.http import errors
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


@pytest.mark.limited
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


@pytest.mark.parametrize('after', [None, 'from_config'])
@pytest.mark.parametrize('before', [None, 'from_config'])
@pytest.mark.parametrize('limit', [None, 1])
async def test_get_guilds(
    limit: int | None,
    before: Literal['from_config'] | int | None,
    after: Literal['from_config'] | int | None,
    users_res: UserResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the current user's guilds."""
    if before == 'from_config':
        before = int(integration_data.guild_id)

    if after == 'from_config':
        after = int(integration_data.guild_id)

    guilds = await users_res.get_guilds(
        limit=limit,
        before=before,
        after=after,
    )
    assert isinstance(guilds, list)


async def test_create_group_dm(
    users_res: UserResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test creating a group DM.

    Just a smoke test to test some models.
    """
    with pytest.raises(errors.ClientError, match='CHANNEL_RECIPIENT_REQUIRED'):
        await users_res.create_group_dm([integration_data.user_id])


@pytest.mark.skip(reason='Bot cannot use this endpoint')
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


async def test_get_connections(
    users_res: UserResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the current user's connections."""
    await users_res.get_current_user_connections()
