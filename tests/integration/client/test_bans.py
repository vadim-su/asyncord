from __future__ import annotations

import pytest

from asyncord.client.bans import BanResource
from asyncord.client.http.errors import ClientError
from asyncord.client.rest import RestClient
from tests.conftest import IntegrationData


@pytest.fixture()
def ban_managment(
    client: RestClient,
    integration_data: IntegrationData
):
    return client.guilds.ban_managment(integration_data.TEST_GUILD_ID)


@pytest.mark.skip(reason='Dangerous operation. Needs manual control.')
async def test_ban_managment(
    ban_managment: BanResource,
    integration_data: IntegrationData
):
    with pytest.raises(ClientError, match=r'\(\d*\) Unknown Ban'):
        await ban_managment.get(integration_data.TEST_USER_TO_BAN)

    bans = await ban_managment.get_list()
    assert not bans

    ban_reason = 'Test ban'
    await ban_managment.ban(integration_data.TEST_USER_TO_BAN, 1, reason=ban_reason)

    # test get ban after ban
    ban = await ban_managment.get(integration_data.TEST_USER_TO_BAN)
    assert ban.user.id == integration_data.TEST_USER_TO_BAN
    assert ban.reason == ban_reason

    # test get list bans after ban
    bans = await ban_managment.get_list()
    assert len(bans) == 1
    assert ban in bans

    # test unban
    await ban_managment.unban(integration_data.TEST_USER_TO_BAN)
    assert not await ban_managment.get_list()


async def test_get_ban_list(ban_managment: BanResource):
    bans = await ban_managment.get_list()
    assert isinstance(bans, list)
