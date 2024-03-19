import pytest
from pydantic import BaseModel

from asyncord.client.models.permissions import PermissionFlag


def test_permission_flag_name_and_value() -> None:
    """Test that PermissionFlag has correct name and value."""
    flag = PermissionFlag.CREATE_INSTANT_INVITE
    assert flag.value == 1
    assert flag.name == 'CREATE_INSTANT_INVITE'


def test_permission_flag_bitwise_operation() -> None:
    """Test that PermissionFlag can be used in bitwise operations."""
    flag1 = PermissionFlag.CREATE_INSTANT_INVITE
    flag2 = PermissionFlag.KICK_MEMBERS
    combined_flags = flag1 | flag2
    assert combined_flags & flag1
    assert combined_flags & flag2


def test_permission_flags_name_and_value() -> None:
    """Test that PermissionFlag has correct name and value."""
    flag1 = PermissionFlag.CREATE_INSTANT_INVITE
    flag2 = PermissionFlag.KICK_MEMBERS
    combined_flags = flag1 | flag2

    assert flag1.value == 1
    assert flag1.name == 'CREATE_INSTANT_INVITE'

    assert flag2.value == 2**1
    assert flag2.name == 'KICK_MEMBERS'

    assert combined_flags.value == 2**0 + 2**1
    assert combined_flags.name == 'CREATE_INSTANT_INVITE|KICK_MEMBERS'


def test_permission_flag_convertation() -> None:
    """Test that PermissionFlag can be converted to int and str."""
    flag = PermissionFlag.CREATE_INSTANT_INVITE | PermissionFlag.KICK_MEMBERS
    assert int(flag) == 2**0 + 2**1
    assert str(flag) == str(2**0 + 2**1)


@pytest.mark.parametrize('permission_type', [PermissionFlag, int, str])
def test_permission_flag_as_part_of_model(permission_type: type) -> None:
    """Test that PermissionFlag can be used as part of pydantic model."""

    class TestModel(BaseModel):
        flag: PermissionFlag

    flag = PermissionFlag.CREATE_INSTANT_INVITE | PermissionFlag.KICK_MEMBERS
    model = TestModel(flag=permission_type(flag))

    assert model.flag == flag
    assert model.model_dump() == {'flag': flag}
    assert model.model_dump(mode='json') == {'flag': str(flag.value)}
