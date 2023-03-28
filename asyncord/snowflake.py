"""A set of auxiliary entities for working with Snowflake."""
from __future__ import annotations

from typing import Any, Final
from datetime import datetime

DISCORD_EPOCH: Final[int] = 1420070400000
"""The start of discord epoch.

The first second of 01.01.2015.
"""


class Snowflake:  # noqa: WPS214 Found too many methods
    """Discord ID.

    It's variant of twitter's snowflake format of IDs.

    See details at:
    https://discord.com/developers/docs/reference#snowflakes
    """

    __slots__ = ('_raw_value',)

    def __init__(self, raw_snowflake: int | str) -> None:
        """Create new snowflake object from raw int.

        Args:
            raw_snowflake (int | str): raw value of snowflake.
        """
        self._raw_value = int(raw_snowflake)

    @classmethod
    def build(
        cls,
        timestamp: int | datetime,
        internal_worker_id: int,
        internal_process_id: int,
        increment: int,
    ) -> Snowflake:
        """Build snowflake from separate parameters.

        Args:
            timestamp (int | datetime): timestamp of snowflake.
            internal_worker_id (int): internal worker id.
            internal_process_id (int): internal process id.
            increment (int): increment of snowflake.

        Returns:
            Snowflake: snowflake object.
        """
        if isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp() * 1000)

        raw_snowflake = (
            (timestamp - DISCORD_EPOCH) << 22
            | internal_worker_id << 17
            | internal_process_id << 12
            | increment
        )
        return Snowflake(raw_snowflake)

    @property
    def timestamp(self) -> datetime:
        """Extract timestamp.

        Milliseconds since Discord Epoch, the first second of 2015 or 1420070400000.
        The first 22 bits of snowflake.

        See details at:
        https://discord.com/developers/docs/reference#snowflakes-snowflake-id-format-structure-left-to-right

        Returns:
            datetime: timestamp.
        """
        timestamp_secs: float = ((self._raw_value >> 22) + DISCORD_EPOCH) / 1000
        return datetime.fromtimestamp(timestamp_secs)

    @property
    def internal_worker_id(self) -> int:
        """Extract internal worker id.

        The next 5 bits after timestamp.

        See details at:
        https://discord.com/developers/docs/reference#snowflakes-snowflake-id-format-structure-left-to-right

        Returns:
            int: internal worker id.
        """
        # ampersand operation removes left first 22 bits of snowflake and takes the rest
        # shift operation removes right 17 zero bits
        return (self._raw_value & 0x3E0000) >> 17  # noqa: WPS432

    @property
    def internal_process_id(self) -> int:
        """Extract nternal process id.

        The next 5 bits after internal worker id.

        See details at:
        https://discord.com/developers/docs/reference#snowflakes-snowflake-id-format-structure-left-to-right

        Returns:
            int: internal process id.
        """
        return (self._raw_value & 0x1F000) >> 12  # noqa: WPS432

    @property
    def increment(self) -> int:
        """Extract increment.

        Last 12 bits of snowflake.

        See details at:
        https://discord.com/developers/docs/reference#snowflakes-snowflake-id-format-structure-left-to-right

        Returns:
            int: increment.
        """
        return self._raw_value & 0xFFF  # noqa: WPS432

    @classmethod
    def validate(cls, value: Any) -> Snowflake:
        """Pydantic auxiliary validation method.

        Args:
            value (Any): value to validate.

        Raises:
            ValueError: if value is not valid snowflake.

        Returns:
            Snowflake: validated snowflake.
        """
        if isinstance(value, (str, int)):
            return cls(value)

        if isinstance(value, cls):
            return value

        raise ValueError('Invalid value type')

    @classmethod
    def __get_validators__(cls):
        """Get validators for pydantic.

        Yields:
            callable: validator.
        """
        yield cls.validate

    def __eq__(self, other: Any) -> bool:
        match other:
            case Snowflake():
                return self._raw_value == other._raw_value
            case int():
                return self._raw_value == other
            case str():
                return str(self._raw_value) == other

        return super().__eq__(other)

    def __int__(self) -> int:
        return self._raw_value

    def __str__(self) -> str:
        return str(self._raw_value)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f'{class_name}({self._raw_value})'

    def __hash__(self) -> int:
        """Hash snowflake.

        Needed for searching with `in` operator. `str` representation used because
        it's most popular type to search for snowflake in lists.

        Returns:
            int: hash of snowflake.
        """
        return hash(str(self._raw_value))
