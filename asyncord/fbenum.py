from enum import Enum
from typing import Final

UNKNOWN: Final[str] = 'UNKNOWN'
"""Fallback name for unknown values."""


class FallbackEnum(Enum):
    """Enum that returns a pseudo-member for unknown values.

    This is useful for enums that are used to represent values from an API.
    Sometimes, the API will return a value that is not in the enum (and docs).
    """

    @classmethod
    def _missing_(cls, value):
        """Return a pseudo-member for the given value.

        This is called by the enum metaclass when no other member matches.
        See how enum.Flag handles unknown values.
        """
        if cls._member_type_ is object:  # type: ignore
            pseudo_member = object.__new__(cls)
        else:
            pseudo_member = cls._member_type_.__new__(cls, value)  # type: ignore
        if not hasattr(pseudo_member, '_value_'):
            pseudo_member._value_ = value
        pseudo_member._name_ = UNKNOWN
        return pseudo_member
