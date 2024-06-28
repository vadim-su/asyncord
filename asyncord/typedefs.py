"""This module contains some useful type definitions and type adapters."""

from __future__ import annotations

import enum
from functools import lru_cache
from typing import TYPE_CHECKING, Literal, NewType

from pydantic import TypeAdapter
from yarl import URL

CURRENT_USER: CurrentUserType = '@me'
"""Literal for the current user endpoint."""

type CurrentUserType = Literal['@me']
"""Type alias for the current user type."""


StrOrURL = URL | str
"""URL in string or yarl.URL format."""

UnsetType = NewType('UnsetType', object)
"""Type of an unset value."""
Unset: UnsetType = UnsetType(object())
"""Sentinel for an unset value.

This value is used to represent an unset value in the API.
It can be used to differentiate between a value that is not set and a value that is set to None.
Sentinels described in draft PEP 601 (https://peps.python.org/pep-0661/).
"""

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
    def _missing_(cls, values: str | set[str]) -> object:  # type: ignore
        """Returns the missing value of the scope.

        Try to get members by values and fail if any value is not found.
        """
        if isinstance(values, str):
            values = {values}

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
        return ' '.join(sorted(self._value_))

    def __str__(self) -> str:
        """Returns the string representation of the scope."""
        return self.value

    def __repr__(self) -> str:
        """Returns the representation of the scope."""
        return f'<{self.__class__.__name__}.{self.name}>'

    def __or__(self, other: StrFlag) -> StrFlag:
        """Returns the union of the two scopes."""
        return self.__class__(self._value_ | other._value_)

    def __eq__(self, other: StrFlag | object) -> bool:
        """Compare two flags."""
        if isinstance(other, StrFlag):
            return sorted(self._value_) == sorted(other._value_)

        return super().__eq__(other)

    def __hash__(self) -> int:
        """Return the hash value of the flag."""
        return hash(self.value)
