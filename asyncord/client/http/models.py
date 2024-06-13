"""HTTP models for the HTTP client."""

from __future__ import annotations

import datetime
import enum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Annotated, Any, BinaryIO, NamedTuple

from fbenum.enum import FallbackEnum
from pydantic import BaseModel, Field

from asyncord.client.http import headers
from asyncord.client.http.error_codes import ErrorCode

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping, Sequence
    from http import HTTPStatus

    import aiohttp

    from asyncord.client.http.headers import HttpMethod
    from asyncord.typedefs import StrOrURL


type ObjectErrorType = dict[str, ErrorBlock | ObjectErrorType | ArrayErrorType]
"""Type hint for an object error."""

type ArrayErrorType = dict[int, ObjectErrorType]
"""Type hint for an array error."""


class Response(NamedTuple):
    """Response structure for the HTTP client."""

    raw_response: aiohttp.ClientResponse
    """Raw response object."""

    status: HTTPStatus
    """Response status code."""

    headers: Mapping[str, str]
    """Response headers."""

    raw_body: bytes
    """Raw response body."""

    body: dict[str, Any]
    """Parsed response body."""


@dataclass
class Request:
    """Request data class."""

    method: HttpMethod
    """HTTP method to use."""

    url: StrOrURL
    """URL to send the request to."""

    payload: Any | None = None
    """Payload to send with the request."""

    files: Sequence[AttachedFile] | None = None
    """Files to send with the request."""

    headers: MutableMapping[str, str] = field(default_factory=dict)
    """Headers to send with the request."""


class AttachedFile(NamedTuple):
    """Type alias for a file to be attached to a request.

    The tuple contains the filename, the content type, and the file object.
    """

    filename: str
    """Name of the file."""

    content_type: str
    """Content type of the file."""

    file: BinaryIO
    """File object."""


class ErrorItem(BaseModel):
    """Represents an error item."""

    code: str
    """Error code."""

    message: str
    """Error message."""


class ErrorBlock(BaseModel):
    """Represents an object error."""

    errors: list[ErrorItem] = Field(alias='_errors')
    """List of errors."""


class ErrorResponse(BaseModel):
    """Represents a body of a response error."""

    code: ErrorCode
    """Error code."""

    message: str
    """Error message."""

    errors: ErrorBlock | ObjectErrorType | None = None
    """Error block."""


class RatelimitResponse(BaseModel):
    """Ratelimit body model."""

    message: str
    """Ratelimit message."""

    retry_after: float
    """Time in seconds to wait before retrying."""

    is_global: Annotated[bool, Field(alias='global')]
    """Whether the ratelimit is global."""

    code: ErrorCode | None = None
    """Error code."""


@enum.unique
class RateLimitScope(enum.StrEnum, FallbackEnum):
    """Rate limit scope."""

    USER = 'user'
    """Rate limit is per bot or user."""

    GLOBAL = 'global'
    """Rate limit is global."""

    SHARED = 'shared'
    """Per resource rate limit."""


class RateLimitHeaders(BaseModel):
    """Rate limit headers model."""

    limit: Annotated[int, Field(alias=headers.RATELIMIT_REQUEST_LIMIT.lower())]
    """Number of requests that can be made."""

    remaining: Annotated[int, Field(alias=headers.RATELIMIT_REQUEST_REMAINING.lower())]
    """Number of remaining requests that can be made."""

    reset: Annotated[datetime.datetime, Field(alias=headers.RATELIMIT_RESET.lower())]
    """Time at which the rate limit will reset in seconds since unix epoch."""

    reset_after: Annotated[float, Field(alias=headers.RATELIMIT_RESET_AFTER.lower())]
    """Time in seconds until the rate limit resets."""

    bucket: Annotated[str, Field(alias=headers.RATELIMIT_BUCKET.lower())]
    """Rate limit bucket."""

    is_global: Annotated[bool | None, Field(alias=headers.RATELIMIT_GLOBAL.lower())] = None
    """Whether the ratelimit is global."""

    scope: Annotated[RateLimitScope | None, Field(alias=headers.RATELIMIT_SCOPE.lower())] = None
