import pytest

from asyncord.client.http import errors
from asyncord.client.members.models.requests import UpdateMemberRequest
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


async def test_list_members(members_res: MemberResource) -> None:
    """Test getting a list of members."""
    member_list = await members_res.get_list(limit=1)
    assert len(member_list) == 1
    assert member_list[0].user
    assert member_list[0].user.id


async def test_search_members(
    members_res: MemberResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test searching for a member."""
    member_list = await members_res.search(nick_or_name='Cuca')
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
    await members_res.add_role(
        user_id=integration_data.member_id,
        role_id=integration_data.role_id,
    )

    member = await members_res.get(integration_data.member_id)
    assert integration_data.role_id in member.roles

    # check role removal
    await members_res.remove_role(
        user_id=integration_data.member_id,
        role_id=integration_data.role_id,
    )

    member = await members_res.get(integration_data.member_id)
    assert integration_data.role_id not in member.roles


@pytest.mark.parametrize(
    'user_id',
    [
        '@me',
        pytest.param(
            'from_config',
            marks=pytest.mark.skip(
                reason=("Function should work, but discord doesn't allow changing nicknames"),
            ),
        ),
    ],
)
async def test_update_member(
    user_id: str,
    members_res: MemberResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test updating a member."""
    if user_id == 'from_config':
        user_id = integration_data.member_id

    new_nickname = 'Cucaracha'
    member = await members_res.update(
        user_id=user_id,
        member_data=UpdateMemberRequest(nick=new_nickname),
    )
    assert member.nick == new_nickname

    # reset to default nickname
    member = await members_res.update(
        user_id=user_id,
        member_data=UpdateMemberRequest(nick=None),
    )

    assert member.nick is None


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


async def test_kick_unkown_user(members_res: MemberResource) -> None:
    """Test kicking a member."""
    with pytest.raises(errors.NotFoundError):
        await members_res.kick('123451231', 'test')
