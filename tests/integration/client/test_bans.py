from __future__ import annotations

import pytest

from asyncord.client.bans.resources import BanResource
from asyncord.client.http import errors
from asyncord.client.http.errors import ClientError
from tests.conftest import IntegrationTestData


@pytest.mark.skip(reason='Dangerous operation. Needs manual control')
async def test_ban_cycle(
    ban_managment: BanResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test the ban managment.

    This test is skipped by default because I have not enough friends to test this.
    """
    with pytest.raises(ClientError, match=r'\(\d*\) Unknown Ban'):
        await ban_managment.get(integration_data.user_to_ban)

    bans = await ban_managment.get_list()
    assert not bans

    ban_reason = 'Test ban'
    await ban_managment.ban(integration_data.user_to_ban, 1, reason=ban_reason)

    # test get ban after ban
    ban = await ban_managment.get(integration_data.user_to_ban)
    assert ban.user.id == integration_data.user_to_ban
    assert ban.reason == ban_reason

    # test get list bans after ban
    bans = await ban_managment.get_list()
    assert len(bans) == 1
    assert ban in bans

    # test unban
    await ban_managment.unban(integration_data.user_to_ban)
    assert not await ban_managment.get_list()

    # test bulk ban and then unban


@pytest.mark.skip(reason='Dangerous operation. Needs manual control')
async def test_bulk_ban(ban_managment: BanResource, integration_data: IntegrationTestData) -> None:
    """Test the bulk ban method."""
    await ban_managment.bulk_ban([integration_data.user_to_ban])
    bans = await ban_managment.get_list()
    assert integration_data.user_to_ban in [ban.user.id for ban in bans]
    await ban_managment.unban(integration_data.user_to_ban)


@pytest.mark.parametrize('delete_message_secs', [None, 1])
async def test_ban_unknown_user(delete_message_secs: int, ban_managment: BanResource) -> None:
    """Test banning an unknown user.

    It's easier to test this with a known user, but someones can be banned.
    """
    with pytest.raises(errors.NotFoundError):
        await ban_managment.ban(
            user_id=12232323232,
            delete_message_seconds=delete_message_secs,
        )


async def test_unban_unknown_user(ban_managment: BanResource) -> None:
    """Test unbanning an unknown user."""
    with pytest.raises(errors.NotFoundError):
        await ban_managment.unban(12232323232)


@pytest.mark.parametrize('delete_message_secs', [None, 1])
async def test_empty_bulk_ban(delete_message_secs: int, ban_managment: BanResource) -> None:
    """Test the bulk ban method with empty list."""
    await ban_managment.bulk_ban(
        user_ids=[],
        delete_message_seconds=delete_message_secs,
    )


async def test_get_ban_of_unknown_user(ban_managment: BanResource) -> None:
    """Test getting a ban of an unknown user."""
    with pytest.raises(errors.NotFoundError):
        await ban_managment.get(12232323232)


@pytest.mark.parametrize('after', [None, 12345])
@pytest.mark.parametrize('before', [None, 12345])
@pytest.mark.parametrize('limit', [None, 1])
async def test_get_ban_list(
    limit: int | None,
    before: int | None,
    after: int | None,
    ban_managment: BanResource,
) -> None:
    """Test the get ban list method."""
    bans = await ban_managment.get_list(
        limit=limit,
        before=before,
        after=after,
    )
    assert isinstance(bans, list)
