from __future__ import annotations

import pytest

from asyncord.client.bans.resources import BanResource
from asyncord.client.http.errors import ClientError
from tests.conftest import IntegrationTestData


@pytest.mark.skip(reason='Dangerous operation. Needs manual control.')
async def test_ban_managment(
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


async def test_get_ban_list(ban_managment: BanResource) -> None:
    """Test the get ban list method."""
    bans = await ban_managment.get_list()
    assert isinstance(bans, list)
