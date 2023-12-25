from asyncord.client.models.roles import CreateRoleData
from asyncord.client.roles import RoleResource


async def test_create_and_delete_role(roles_res: RoleResource):
    new_role_name = 'TestRole'
    role = await roles_res.create(CreateRoleData(name=new_role_name))
    assert role.name == new_role_name
    await roles_res.delete(role.id)


async def test_get_role_list(roles_res: RoleResource):
    role_list = await roles_res.get_list()
    assert role_list
    assert role_list[0].id
    assert role_list[0].name
