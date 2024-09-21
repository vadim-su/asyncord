from collections.abc import AsyncGenerator

import pytest

from asyncord.client.roles.models.requests import CreateRoleRequest, RolePositionRequest, UpdateRoleRequest
from asyncord.client.roles.models.responses import RoleResponse
from asyncord.client.roles.resources import RoleResource


@pytest.fixture
async def role(roles_res: RoleResource) -> AsyncGenerator[RoleResponse, None]:
    """Create a role and delete it after the test."""
    role = await roles_res.create(CreateRoleRequest(name='TestRole'))
    yield role
    await roles_res.delete(role.id)


async def test_get_role_list(roles_res: RoleResource) -> None:
    """Test getting a list of roles."""
    role_list = await roles_res.get_list()
    assert role_list
    assert role_list[0].id
    assert role_list[0].name


async def test_change_role_positions(role: RoleResponse, roles_res: RoleResource) -> None:
    """Test changing the position of a role."""
    roles = await roles_res.change_role_positions(
        [
            RolePositionRequest(
                id=role.id,
                position=2,
            ),
        ],
    )

    updated_role = next(filter(lambda r: r.id == role.id, roles))
    assert updated_role.position == 2


async def test_update_role(role: RoleResponse, roles_res: RoleResource) -> None:
    """Test updating a role."""
    role = await roles_res.update_role(
        role_id=role.id,
        role_data=UpdateRoleRequest(name='UpdatedRole'),
    )
    assert role.name == 'UpdatedRole'
