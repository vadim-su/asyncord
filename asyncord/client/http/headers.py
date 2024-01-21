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

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
