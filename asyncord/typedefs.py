from functools import lru_cache
from typing import TYPE_CHECKING, TypeVar
from pydantic import TypeAdapter
from yarl import URL

from asyncord.snowflake import Snowflake

StrOrURL = str | URL
LikeSnowflake = int | str | Snowflake


_ListItemType = TypeVar('_ListItemType')

if TYPE_CHECKING:
    def list_model(type_: type[_ListItemType]) -> TypeAdapter[list[_ListItemType]]:
        return TypeAdapter(list[type_])
else:
    @lru_cache()
    def list_model(type_: type[_ListItemType]) -> TypeAdapter[list[_ListItemType]]:
        return TypeAdapter(list[type_])


class MissingType:
    """Sentinel for missing values."""

    __slots__ = ()

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return '<missing>'


MISSING = MissingType()
