import pytest

from asyncord.client.http.errors import ClientError
from asyncord.client.members.resources import MemberResource
from tests.conftest import IntegrationTestData


async def test_get_member(
    members_res: MemberResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting a member."""
    member = await members_res.get(integration_data.member_id)
    assert member.user
    assert member.user.id == integration_data.member_id


@pytest.mark.skip(reason='Need OAUTH GUILD_MEMBERS permission to access members list')
async def test_list_members(members_res: MemberResource) -> None:
    """Test getting a list of members."""
    member_list = await members_res.get_list(limit=1)
    assert len(member_list) == 1
    assert member_list[0].user
    assert member_list[0].user.id


@pytest.mark.skip(reason='Need OAUTH GUILD_MEMBERS permission to access members list')
async def test_search_members(
    members_res: MemberResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test searching for a member."""
    member_list = await members_res.search('Cucaryamba')
    assert len(member_list) == 1
    assert member_list[0].user
    assert member_list[0].user.id == integration_data.member_id


async def test_update_current_member(members_res: MemberResource) -> None:
    """Test updating the current member."""
    new_nickname = 'Cucaracha'
    member = await members_res.update_current_member(nickname=new_nickname)
    assert member.nick == new_nickname
    # reset to default nickname
    await members_res.update_current_member(nickname=None)


async def test_role_operations(
    members_res: MemberResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test adding and removing a role."""
    # check role addition
    await members_res.add_role(integration_data.member_id, integration_data.role_id)

    member = await members_res.get(integration_data.member_id)
    assert integration_data.role_id in member.roles

    # check role removal
    await members_res.remove_role(integration_data.member_id, integration_data.role_id)

    member = await members_res.get(integration_data.member_id)
    assert integration_data.role_id not in member.roles


@pytest.mark.skip(reason='Dangerous operation. Needs manual control.')
async def test_kick(
    members_res: MemberResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test kicking a member."""
    verum_user_id = integration_data.user_to_ban
    member = await members_res.get(verum_user_id)
    assert member.user
    await members_res.kick(verum_user_id, 'test')

    with pytest.raises(ClientError, match=r'\(\d*\) Unknown Member'):
        member = await members_res.get(verum_user_id)
