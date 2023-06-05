from pydantic import BaseModel
import pytest

from asyncord.client.models.permissions import PermissionFlag


def test_permission_flag_name_and_value():
    flag = PermissionFlag.CREATE_INSTANT_INVITE
    assert flag.value == 1
    assert flag.name == 'CREATE_INSTANT_INVITE'


def test_permission_flag_bitwise_operation():
    flag1 = PermissionFlag.CREATE_INSTANT_INVITE
    flag2 = PermissionFlag.KICK_MEMBERS
    combined_flags = flag1 | flag2
    assert combined_flags & flag1
    assert combined_flags & flag2


def test_permission_flags_name_and_value():
    flag1 = PermissionFlag.CREATE_INSTANT_INVITE
    flag2 = PermissionFlag.KICK_MEMBERS
    combined_flags = flag1 | flag2

    assert flag1.value == 1
    assert flag1.name == 'CREATE_INSTANT_INVITE'

    assert flag2.value == 2**1
    assert flag2.name == 'KICK_MEMBERS'

    assert combined_flags.value == 2**0 + 2**1
    assert combined_flags.name == 'CREATE_INSTANT_INVITE|KICK_MEMBERS'


def test_permission_flag_convertation():
    flag = PermissionFlag.CREATE_INSTANT_INVITE | PermissionFlag.KICK_MEMBERS
    assert int(flag) == 2**0 + 2**1
    assert str(flag) == str(2**0 + 2**1)


@pytest.mark.xfail(raises=AssertionError, reason='Pydantic 2.0b2 was broken')
@pytest.mark.parametrize('permission_type', [PermissionFlag, int, str])
def test_permission_flag_as_part_of_model(permission_type: type):
    class TestModel(BaseModel):
        flag: PermissionFlag
    flag = PermissionFlag.CREATE_INSTANT_INVITE | PermissionFlag.KICK_MEMBERS
    model = TestModel(flag=permission_type(flag))

    assert model.flag == flag
    assert model.model_dump() == {'flag': flag}
    assert model.model_dump(mode='json') == {'flag': str(flag)}
