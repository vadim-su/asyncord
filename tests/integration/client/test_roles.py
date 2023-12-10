import os

import pytest

from asyncord.client.models.roles import CreateRoleData
from asyncord.client.rest import RestClient
from asyncord.client.roles import RoleResource

TEST_GUILD_ID = os.environ.get('TEST_GUILD_ID')


class TestRoles:
    @pytest.fixture()
    async def roles(self, client: RestClient):
        return client.guilds.roles(TEST_GUILD_ID)

    async def test_create_and_delete_role(self, roles: RoleResource):
        new_role_name = 'TestRole'
        role = await roles.create(CreateRoleData(name=new_role_name))
        assert role.name == new_role_name
        await roles.delete(role.id)

    async def test_get_role_list(self, roles: RoleResource):
        role_list = await roles.get_list()
        assert role_list
        assert role_list[0].id
        assert role_list[0].name
