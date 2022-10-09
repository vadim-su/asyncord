from __future__ import annotations

import pytest

from asyncord.client.bans import BanResource
from asyncord.client.rest import RestClient
from asyncord.client.client_errors import ClientError

TEST_GUILD_ID = '763522265874694144'
TEST_MEMBER_ID = '934564225769148436'
TEST_ROLE_ID = '1010835042957787181'


@pytest.fixture()
def ban_managment(client: RestClient):
    return client.guilds.ban_managment(TEST_GUILD_ID)


@pytest.mark.skip(reason='Dangerous operation. Needs manual control.')
async def test_ban_managment(ban_managment: BanResource):
    verum_user_id = '559629484442255370'
    with pytest.raises(ClientError, match=r'\(\d*\) Unknown Ban'):
        await ban_managment.get(verum_user_id)

    bans = await ban_managment.get_list()
    assert not bans

    ban_reason = 'Test ban'
    await ban_managment.ban(verum_user_id, 1, reason=ban_reason)

    # test get ban after ban
    ban = await ban_managment.get(verum_user_id)
    assert ban.user.id == verum_user_id
    assert ban.reason == ban_reason

    # test get list bans after ban
    bans = await ban_managment.get_list()
    assert len(bans) == 1
    assert ban in bans

    # test unban
    await ban_managment.unban(verum_user_id)
    assert not await ban_managment.get_list()
