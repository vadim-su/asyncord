"""This module contains some useful type definitions and type adapters."""

from functools import lru_cache
from typing import TYPE_CHECKING, Any, NewType

from pydantic import TypeAdapter
from yarl import URL

from asyncord.snowflake import Snowflake

StrOrURL = str | URL
LikeSnowflake = Snowflake | int | str
Payload = NewType('Payload', Any)


# Fix for pydanitc and pylance. Pylance doesn't correctly infer the type
# of the list_model function.
if TYPE_CHECKING:

    def list_model[ListItemType](type_: type[ListItemType]) -> TypeAdapter[list[ListItemType]]:
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
    def list_model[ListItemType](type_: type[ListItemType]) -> TypeAdapter[list[ListItemType]]:
        """Return a type adapter for a list of a specific type."""
        return TypeAdapter(list[type_])
