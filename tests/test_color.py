import pytest
from pydantic import BaseModel

from asyncord.color import RGB, Color, ColorInput

DECIMAL_VALUE = 11189196
"""Decimal value of the color."""


@pytest.fixture
def color() -> Color:
    """Return a color object."""
    return Color(0xAABBCC)


def test_rgb_repr() -> None:
    """Test the string representation of an RGB object."""
    assert repr(RGB(170, 187, 204)) == 'RGB(170, 187, 204)'


def test_create_color_from_constructor(color: Color) -> None:
    """Test creating a color from the constructor."""
    assert Color(0xAABBCC).value == DECIMAL_VALUE


@pytest.mark.parametrize(
    'color_value',
    [
        11189196,
        0xAABBCC,  # noqa: PT014
        'aabbcc',
        '0xaabbcc',
        '#aabbcc',
        (170, 187, 204),
        RGB(170, 187, 204),
    ],
    ids=[
        'int',
        'hex int',
        'hex str',
        '0x prefix hex str',
        'web hex str',
        'rgb tuple',
        'RGB class',
    ],
)
def test_create_color(color_value: int | str | RGB | tuple[int, int, int]) -> None:
    """Test creating a color from various values."""
    color = Color.build(color_value)
    assert color.value == DECIMAL_VALUE


def test_compare_colors(color: Color) -> None:
    """Test comparing colors."""
    assert color == Color(DECIMAL_VALUE)
    assert color != Color(0x000000)
    assert color != DECIMAL_VALUE


def test_color_to_int(color: Color) -> None:
    """Test converting a color to an integer."""
    assert int(color) == DECIMAL_VALUE


def test_color_to_str(color: Color) -> None:
    """Test converting a color to a string."""
    assert color.to_hex() == '0xaabbcc'


def test_color_to_rgb(color: Color) -> None:
    """Test converting a color to an RGB tuple."""
    assert color.to_rgb() == RGB(170, 187, 204)


def test_color_repr(color: Color) -> None:
    """Test the string representation of a color."""
    assert repr(color) == f'Color({hex(DECIMAL_VALUE)})'


@pytest.mark.parametrize(
    'color_value',
    [
        11189196,
        0xAABBCC,  # noqa: PT014
        'aabbcc',
        '0xaabbcc',
        '#aabbcc',
        (170, 187, 204),
        RGB(170, 187, 204),
        Color(DECIMAL_VALUE),
    ],
    ids=[
        'int',
        'hex int',
        'hex str',
        '0x prefix hex str',
        'web hex str',
        'rgb tuple',
        'RGB class',
        'Color class',
    ],
)
def test_color_in_models(
    color_value: int | str | RGB | tuple[int, int, int],
    color: Color,
) -> None:
    """Test that the ColorInput type works in Pydantic models."""

    class TestModel(BaseModel):
        color: ColorInput

    model = TestModel(color=color_value)
    assert isinstance(model.color, Color)
    assert model.color == color

    assert model.model_dump() == {'color': color}
    assert model.model_dump(mode='json') == {'color': DECIMAL_VALUE}


def test_color_error_in_models() -> None:
    """Test that the ColorInput type raises an error when given an invalid value."""

    class TestModel(BaseModel):
        color: ColorInput

    with pytest.raises(ValueError, match='invalid literal'):
        TestModel(color='not a color')
