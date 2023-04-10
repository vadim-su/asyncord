from __future__ import annotations

import pytest

from asyncord.client.rest import RestClient
from asyncord.client.members import MemberResource
from asyncord.client.http.errors import ClientError

TEST_GUILD_ID = '763522265874694144'
TEST_MEMBER_ID = '934564225769148436'
TEST_ROLE_ID = '1010835042957787181'


class TestMembers:
    @pytest.fixture()
    async def members(self, client: RestClient):
        return client.guilds.members(TEST_GUILD_ID)

    async def test_get_member(self, members: MemberResource):
        member = await members.get(TEST_MEMBER_ID)
        assert member.user
        assert member.user.id == TEST_MEMBER_ID

    # FIXME: this test needs OAUTH GUILD_MEMBERS permission to access members list
    @pytest.mark.skip(reason='Need OAUTH GUILD_MEMBERS permission to access members list')
    async def test_list_members(self, members: MemberResource):
        member_list = await members.list(limit=1)
        assert len(member_list) == 1
        assert member_list[0].user
        assert member_list[0].user.id

    # FIXME: this test needs OAUTH GUILD_MEMBERS permission to access members list
    @pytest.mark.skip(reason='Need OAUTH GUILD_MEMBERS permission to access members list')
    async def test_search_members(self, members: MemberResource):
        member_list = await members.search('Cucaryamba')
        assert len(member_list) == 1
        assert member_list[0].user
        assert member_list[0].user.id == TEST_MEMBER_ID

    async def test_update_current_member(self, members: MemberResource):
        new_nickname = 'Cucaracha'
        member = await members.update_current_member(new_nickname)
        assert member.nick == new_nickname
        # reset to default nickname
        await members.update_current_member(None)

    async def test_add_and_remove_role(self, members: MemberResource):
        member = await members.get(TEST_MEMBER_ID)
        assert TEST_ROLE_ID not in member.roles

        # check role addition
        await members.add_role(TEST_MEMBER_ID, TEST_ROLE_ID)

        member = await members.get(TEST_MEMBER_ID)
        assert TEST_ROLE_ID in member.roles

        # check role removal
        await members.remove_role(TEST_MEMBER_ID, TEST_ROLE_ID)

        member = await members.get(TEST_MEMBER_ID)
        assert TEST_ROLE_ID not in member.roles

    @pytest.mark.skip(reason='Dangerous operation. Needs manual control.')
    async def test_kick(self, members: MemberResource):
        verum_user_id = '559629484442255370'
        member = await members.get(verum_user_id)
        assert member.user
        await members.kick(verum_user_id, 'test')

        with pytest.raises(ClientError, match=r'\(\d*\) Unknown Member'):
            member = await members.get(verum_user_id)
