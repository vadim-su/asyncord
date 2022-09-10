from __future__ import annotations

from http import HTTPStatus

import pytest

from asyncord.client.rest import RestClient
from asyncord.client.users import UserResource

TEST_GUILD_ID = '763522265874694144'
TEST_USER_ID = '760541547074027573'


class TestUsers:
    @pytest.fixture()
    async def users(self, client: RestClient):
        yield client.users

    async def test_get_current_user(self, users: UserResource):
        user = await users.get_current_user()
        assert user.id

    async def test_get_user(self, users: UserResource):
        current_user = await users.get_current_user()
        user = await users.get_user(current_user.id)
        assert user.id == current_user.id

    @pytest.mark.limited
    async def test_change_current_user_nickname(self, users: UserResource):
        new_nickname = 'Cucaracha'
        resp = await users.update_user(new_nickname)
        assert resp.status == HTTPStatus.OK
        assert resp.body['username'] == new_nickname
        # reset the nickname because i like Cucaryamba
        resp = await users.update_user('Cucaryamba')

    async def test_get_guilds(self, users: UserResource):
        guilds = await users.get_guilds()
        assert len(guilds)
        assert guilds[0].id

    @pytest.mark.skip(reason='Skip the test because bots cannot use this endpoint')
    async def test_get_current_user_guild_member(self, users: UserResource):
        member = await users.get_current_user_guild_member(TEST_GUILD_ID)
        assert member.user
        assert member.user.id == TEST_USER_ID

    async def test_create_dm(self, users: UserResource):
        channel = await users.create_dm(TEST_USER_ID)
        recipients = channel.recipients
        assert recipients
        assert len(recipients)
        assert TEST_USER_ID in {recipient.id for recipient in recipients}
