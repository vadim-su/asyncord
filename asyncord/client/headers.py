# pyright: reportSelfClsParameterName=false
from __future__ import annotations

import enum
from typing import Final

AUTHORIZATION: Final[str] = 'Authorization'
AUDIT_LOG_REASON: Final[str] = 'X-Audit-Log-Reason'


@enum.unique
class HttpMethod(str, enum.Enum):  # noqa: WPS600 Found subclassing a builtin: str
    def _generate_next_value_(name, _start, _count, _last_values):  # noqa: WPS120 trailing underscore
        return name

    GET = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    PATCH = enum.auto()
    DELETE = enum.auto()
