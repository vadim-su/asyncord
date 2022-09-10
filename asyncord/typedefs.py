from yarl import URL

from asyncord.snowflake import Snowflake

StrOrURL = str | URL
LikeSnowflake = int | str | Snowflake


class MissingType:
    """Sentinel for missing values."""

    __slots__ = ()

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return '<missing>'


MISSING = MissingType()
