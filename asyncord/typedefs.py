"""This module contains some useful type definitions and type adapters."""

from __future__ import annotations

import enum
from functools import lru_cache
from typing import TYPE_CHECKING

from pydantic import TypeAdapter
from yarl import URL

StrOrURL = str | URL


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


class StrFlag(str, enum.Enum):  # noqa: UP042
    """String flag enum that allows for bitwise operations."""

    def __init__(self, obj_value: str | set[str]):
        """Initializes the scope with the given value."""
        if isinstance(obj_value, str):
            self._value_ = {obj_value}
        else:
            self._value_ = obj_value

    @classmethod
    def _missing_(cls, values: set[str]) -> object:
        """Returns the missing value of the scope."""
        # get members by values and fail if any value is not found
        actual_members = []
        for value in values:
            member = cls._value2member_map_.get(value)
            if not member:
                raise ValueError(f'{cls.__name__} has no member {value!r}')
            actual_members.append(member)
        actual_members.sort(key=lambda member: member._sort_order_)

        # generate a pseudo-member for combined flags
        # look at enum.Flag._missing_ for more information
        if cls._member_type_ is object:  # type: ignore
            # construct a singleton enum pseudo-member
            pseudo_member = object.__new__(cls)
        else:
            pseudo_member = cls._member_type_.__new__(cls, value)  # type: ignore

        pseudo_member._name_ = '|'.join(member.name for member in actual_members)

        if not hasattr(pseudo_member, '_value_'):
            pseudo_member._value_ = values

        return pseudo_member

    @property
    def value(self) -> str:
        """Returns the value of the scope."""
        return ' '.join(self._value_)

    def __str__(self) -> str:
        """Returns the string representation of the scope."""
        return self.value

    def __repr__(self) -> str:
        """Returns the representation of the scope."""
        return f'<{self.__class__.__name__}.{self.name}>'

    def __or__(self, other: StrFlag) -> StrFlag:
        """Returns the union of the two scopes."""
        return self.__class__(self._value_ | other._value_)

    def _separated_flags(self) -> list[StrFlag]:
        """Returns the separated flags of the scope."""
        return [self.__class__(value) for value in self._value_]
