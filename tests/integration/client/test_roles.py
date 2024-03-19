from asyncord.client.roles.models.requests import CreateRoleRequest
from asyncord.client.roles.resources import RoleResource


async def test_create_and_delete_role(roles_res: RoleResource) -> None:
    """Test creating and deleting a role."""
    new_role_name = 'TestRole'
    role = await roles_res.create(CreateRoleRequest(name=new_role_name))
    assert role.name == new_role_name
    await roles_res.delete(role.id)


async def test_get_role_list(roles_res: RoleResource) -> None:
    """Test getting a list of roles."""
    role_list = await roles_res.get_list()
    assert role_list
    assert role_list[0].id
    assert role_list[0].name
