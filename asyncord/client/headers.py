# pyright: reportSelfClsParameterName=false
from __future__ import annotations

import enum
from typing import Final


@enum.unique
class HttpMethod(str, enum.Enum):  # noqa: WPS600 Found subclassing a builtin: strflake8
    def _generate_next_value_(name, _start, _count, _last_values):  # noqa: WPS120 name with trailing underscore
        return name

    GET = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    PATCH = enum.auto()
    DELETE = enum.auto()


AUTHORIZATION: Final[str] = 'Authorization'
AUDIT_LOG_REASON: Final[str] = 'X-Audit-Log-Reason'
