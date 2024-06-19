import pytest

from asyncord.typedefs import StrFlag


class _TestStrFlag(StrFlag):
    """Test string flag enum."""

    TEST1 = 'test1'
    TEST2 = 'test2'
    TEST3 = 'test3'


@pytest.mark.parametrize(
    'flag',
    [
        pytest.param('no_flag', id='unknown_flag'),
        pytest.param({'no_flag'}, id='unknown_flag_set'),
        pytest.param({'no_flag1', 'no_flag2'}, id='unknown_flag_set_multiple'),
        pytest.param({'test1', 'no_flag'}, id='flag_set_with_existing_flag_and_unknown_flag'),
    ],
)
def test_get_with_unknown_value(flag: str) -> None:
    """Test getting the value of the scope with unknown value."""
    with pytest.raises(ValueError, match='has no member'):
        _TestStrFlag(flag)


@pytest.mark.parametrize(
    'flag',
    [
        pytest.param('test1', id='string_flag'),
        pytest.param({'test1'}, id='flag_set'),
        pytest.param({'test1', 'test2'}, id='flag_set_multiple'),
    ],
)
def test_get_with_value(flag: str) -> None:
    """Test getting the value of the scope."""
    assert _TestStrFlag(flag)._value_ == (flag if isinstance(flag, set) else {flag})


def test_get_value() -> None:
    """Test value of the scope."""
    assert _TestStrFlag['TEST1']
    with pytest.raises(KeyError):
        _TestStrFlag['NO_FLAG']


def test_str() -> None:
    """Test string representation of the scope."""
    assert str(_TestStrFlag.TEST1) == 'test1'
    assert str(_TestStrFlag({'test1', 'test2'})) == 'test1 test2'


def test_repr() -> None:
    """Test representation of the scope."""
    assert repr(_TestStrFlag.TEST1) == '<_TestStrFlag.TEST1>'
    assert repr(_TestStrFlag({'test1', 'test2'})) == '<_TestStrFlag.TEST1|TEST2>'


@pytest.mark.parametrize(
    ('flag1', 'flag2', 'expected'),
    [
        pytest.param(
            _TestStrFlag.TEST1,
            _TestStrFlag.TEST1,
            _TestStrFlag.TEST1,
            id='same_flag',
        ),
        pytest.param(
            _TestStrFlag.TEST1,
            _TestStrFlag.TEST2,
            _TestStrFlag({'test1', 'test2'}),
            id='different_flag',
        ),
        pytest.param(
            _TestStrFlag({'test1', 'test2'}),
            _TestStrFlag.TEST1,
            _TestStrFlag({'test1', 'test2'}),
            id='flag_set_and_same_flag',
        ),
        pytest.param(
            _TestStrFlag({'test1', 'test2'}),
            _TestStrFlag({'test2', 'test3'}),
            _TestStrFlag({'test1', 'test2', 'test3'}),
            id='flag_set_and_flag_set',
        ),
        pytest.param(
            _TestStrFlag({'test1', 'test2'}),
            _TestStrFlag({'test2', 'test3'}),
            _TestStrFlag({'test1', 'test2', 'test3'}),
            id='flag_set_and_flag_set_union',
        ),
    ],
)
def test_concatenation(flag1: _TestStrFlag, flag2: _TestStrFlag, expected: _TestStrFlag) -> None:
    """Test the union of the two scopes."""
    assert (flag1 | flag2) == expected
