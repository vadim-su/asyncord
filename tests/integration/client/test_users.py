from http import HTTPStatus

import pytest

from asyncord.client.users.resources import UserResource
from tests.conftest import IntegrationTestData


async def test_get_current_user(users_res: UserResource):
    user = await users_res.get_current_user()
    assert user.id


async def test_get_user(users_res: UserResource):
    current_user = await users_res.get_current_user()
    user = await users_res.get_user(current_user.id)
    assert user.id == current_user.id


@pytest.mark.limited
async def test_change_current_user_nickname(users_res: UserResource):
    new_nickname = 'Cucaracha'
    resp = await users_res.update_user(new_nickname)
    assert resp.status == HTTPStatus.OK
    assert resp.body['username'] == new_nickname
    # reset the nickname because i like Cucaryamba
    resp = await users_res.update_user('Cucaryamba')


async def test_get_guilds(users_res: UserResource):
    guilds = await users_res.get_guilds()
    assert len(guilds)
    assert guilds[0].id


@pytest.mark.skip(reason='Skip the test because bots cannot use this endpoint')
async def test_get_current_user_guild_member(users_res: UserResource, integration_data: IntegrationTestData):
    member = await users_res.get_current_user_guild_member(integration_data.guild_id)
    assert member.user
    assert member.user.id


async def test_create_dm(users_res: UserResource, integration_data: IntegrationTestData):
    channel = await users_res.create_dm(integration_data.user_id)
    recipients = channel.recipients
    assert recipients
    assert len(recipients)
    assert integration_data.user_id in {recipient.id for recipient in recipients}
