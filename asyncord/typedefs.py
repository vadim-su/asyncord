"""This module contains some useful type definitions and type adapters."""

from functools import lru_cache
from typing import TYPE_CHECKING, Any, NewType, TypeVar

from pydantic import TypeAdapter
from yarl import URL

from asyncord.snowflake import Snowflake

StrOrURL = str | URL
LikeSnowflake = int | str | Snowflake
Payload = NewType('Payload', Any)


_ListItemType = TypeVar('_ListItemType')

# Fix for pydanitc and pylance. Pylance don't correctly infer the type
# of the list_model function.
if TYPE_CHECKING:
    def list_model(type_: type[_ListItemType]) -> TypeAdapter[list[_ListItemType]]:
        """Return a type adapter for a list of a specific type.

        Example:
            >>> from asyncord.typedefs import list_model
            >>> from pydantic import BaseModel
            >>> class Foo(BaseModel):
            ...     bar: str
            >>> list_model(Foo).validate_python([{'bar': 'baz'}])
            [Foo(bar='baz')]
        """
        return TypeAdapter(list[type_])
else:
    @lru_cache
    def list_model(type_: type[_ListItemType]) -> TypeAdapter[list[_ListItemType]]:
        """Return a type adapter for a list of a specific type."""
        return TypeAdapter(list[type_])
