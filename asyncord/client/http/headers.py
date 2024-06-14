"""Module containing HTTP headers constants."""

from __future__ import annotations

import enum
from typing import Final

AUTHORIZATION: Final[str] = 'Authorization'
AUDIT_LOG_REASON: Final[str] = 'X-Audit-Log-Reason'

JSON_CONTENT_TYPE: Final[str] = 'application/json'


# region Rate limit headers
RATELIMIT_REQUEST_LIMIT: Final[str] = 'X-RateLimit-Limit'
"""Number of requests that can be made to the endpoint."""

RATELIMIT_REQUEST_REMAINING: Final[str] = 'X-RateLimit-Remaining'
"""Number of requests that can still be made."""

RATELIMIT_RESET: Final[str] = 'X-RateLimit-Reset'
"""Time at which the rate limit will reset in seconds since unix epoch."""

RATELIMIT_RESET_AFTER: Final[str] = 'X-RateLimit-Reset-After'
"""Time in seconds until the rate limit resets."""

RATELIMIT_BUCKET: Final[str] = 'X-RateLimit-Bucket'
"""Bucket the rate limit is for."""

RATELIMIT_GLOBAL: Final[str] = 'X-RateLimit-Global'
"""Whether the rate limit is global."""

RATELIMIT_SCOPE: Final[str] = 'X-RateLimit-Scope'
"""Rate limit scope."""
# endregion Rate limit headers


@enum.unique
class HttpMethod(enum.StrEnum):
    """HTTP methods which we use in the client."""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
