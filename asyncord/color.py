"""Module that provides a color class for discord."""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, Any, Final, NamedTuple, Self

from pydantic import BaseModel
from pydantic_core import CoreSchema, core_schema


class RGB(NamedTuple):
    """Class that represents an RGB color."""

    red: int
    """Red value of the color."""

    green: int
    """Green value of the color."""

    blue: int
    """Blue value of the color."""

    def __repr__(self) -> str:
        """Return a string representation of the RGB object."""
        return f'RGB({self.red}, {self.green}, {self.blue})'


class Color:
    """Class that represents a color in discord."""

    def __init__(self, value: int):
        """Initialize the color with an integer value.

        Args:
            value: Integer value of the color.
        """
        self.value = value

    @classmethod
    def build(cls, value: int | str | RGB | tuple[int, int, int]) -> Self:
        """Create a color from red, green, and blue values."""
        match value:
            case int():
                return cls(value)
            case str():
                return cls(int(value.lstrip('#'), 16))
            case RGB():
                return cls((value.red << 16) + (value.green << 8) + value.blue)
            case red, green, blue if isinstance(red, int) and isinstance(green, int) and isinstance(blue, int):
                return cls((red << 16) + (green << 8) + blue)

        raise ValueError('Invalid value type')

    def to_rgb(self) -> RGB:
        """Return the red, green, and blue values of the color."""
        return RGB(
            red=(self.value >> 16) & 255,
            green=(self.value >> 8) & 255,
            blue=self.value & 255,
        )

    def to_hex(self) -> str:
        """Return the hexadecimal code of the color."""
        return hex(self.value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: type[BaseModel],
        _handler: Callable[[Any], CoreSchema],
    ) -> CoreSchema:
        """Pydantic auxiliary method to get schema.

        Args:
            _source: Source of schema.
            _handler: Handler of schema.

        Returns:
            Pydantic core schema.
        """
        schema = core_schema.union_schema([
            core_schema.int_schema(),
            core_schema.str_schema(),
            core_schema.is_instance_schema(RGB),
            core_schema.tuple_positional_schema([
                core_schema.int_schema(),
                core_schema.int_schema(),
                core_schema.int_schema(),
            ]),
            core_schema.is_instance_schema(cls),
        ])

        return core_schema.no_info_after_validator_function(
            function=cls._validate,
            schema=schema,
            serialization=core_schema.plain_serializer_function_ser_schema(
                function=cls._serialize,
                when_used='json-unless-none',
            ),
        )

    def __repr__(self) -> str:
        """Return a string representation of the color object."""
        return f'Color({self.to_hex()})'

    def __eq__(self, other: Color) -> bool:
        """Compare two colors for equality."""
        if not isinstance(other, Color):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Return the hash value of the color object."""
        return hash(self.value)

    def __int__(self) -> int:
        """Return the integer value of the color."""
        return self.value

    @classmethod
    def _validate(cls, value: int | str | RGB | tuple[int, int, int] | Self) -> Self:
        """Pydantic auxiliary validation method.

        Args:
            value: Value to validate.

        Returns:
            Validated Color.

        Raises:
            ValueError: If value is not
        """
        if isinstance(value, int | str | RGB):
            return cls.build(value)

        # fmt: off
        if (
            isinstance(value, tuple)
            and len(value) == 3  # noqa: PLR2004
            and all(isinstance(v, int) for v in value)
        ):
            return cls.build(value)
        # fmt: on

        if isinstance(value, cls):
            return value

        raise ValueError('Invalid value type')

    @classmethod
    def _serialize(cls, value: Self) -> int:
        """Pydantic auxiliary method to serialize the color.

        Args:
            value: Value to serialize.

        Returns:
            Serialized value.
        """
        return int(value)


type ColorInput = Annotated[int | str | RGB | tuple[int, int, int] | Color, Color]
"""Color input type."""

# Define some color constants for convenience

DEFAULT_COLOR: Final[Color] = Color(0)
TEAL: Final[Color] = Color(0x1ABC9C)
DARK_TEAL: Final[Color] = Color(0x11806A)
GREEN: Final[Color] = Color(0x2ECC71)
DARK_GREEN: Final[Color] = Color(0x1F8B4C)
BLUE: Final[Color] = Color(0x3498DB)
DARK_BLUE: Final[Color] = Color(0x206694)
PURPLE: Final[Color] = Color(0x9B59B6)
DARK_PURPLE: Final[Color] = Color(0x71368A)
MAGENTA: Final[Color] = Color(0xE91E63)
DARK_MAGENTA: Final[Color] = Color(0xAD1457)
GOLD: Final[Color] = Color(0xF1C40F)
DARK_GOLD: Final[Color] = Color(0xC27C0E)
ORANGE: Final[Color] = Color(0xE67E22)
DARK_ORANGE: Final[Color] = Color(0xA84300)
RED: Final[Color] = Color(0xE74C3C)
DARK_RED: Final[Color] = Color(0x992D22)
LIGHTER_GREY: Final[Color] = Color(0x95A5A6)
DARK_GREY: Final[Color] = Color(0x607D8B)
LIGHT_GREY: Final[Color] = Color(0x979C9F)
DARKER_GREY: Final[Color] = Color(0x546E7A)
BLURPLE: Final[Color] = Color(0x5865F2)
GREYPLE: Final[Color] = Color(0x99AAB5)
DARK_THEME: Final[Color] = Color(0x36393F)
