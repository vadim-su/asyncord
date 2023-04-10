# pyright: reportSelfClsParameterName=false
from __future__ import annotations

import enum
from typing import Final

AUTHORIZATION: Final[str] = 'Authorization'
AUDIT_LOG_REASON: Final[str] = 'X-Audit-Log-Reason'
JSON_CONTENT_TYPE: Final[str] = 'application/json'


@enum.unique
class HttpMethod(enum.StrEnum):
    """HTTP method enum."""

    # ignore argument of a method should be named 'self' and trailing underscore
    def _generate_next_value_(name: str, _start, _count, _last_values) -> str:  # noqa: N805, WPS120
        return name

    GET = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    PATCH = enum.auto()
    DELETE = enum.auto()
