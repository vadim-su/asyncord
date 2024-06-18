"""HTTP models for the HTTP client."""

from __future__ import annotations

import datetime
import enum
import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from http import HTTPStatus
from io import BufferedReader, IOBase
from pathlib import Path
from typing import Annotated, Any, NamedTuple

import aiohttp
from fbenum.enum import FallbackEnum
from pydantic import BaseModel, Field, JsonValue

from asyncord.client.http import headers
from asyncord.client.http.error_codes import ErrorCode
from asyncord.typedefs import StrOrURL

__all__ = (
    'ArrayErrorType',
    'ErrorBlock',
    'ErrorItem',
    'ErrorResponse',
    'FieldValueType',
    'FormField',
    'FormPayload',
    'ObjectErrorType',
    'RateLimitHeaders',
    'RateLimitScope',
    'RatelimitResponse',
    'Request',
    'Response',
)

type ObjectErrorType = dict[str, ErrorBlock | ObjectErrorType | ArrayErrorType]
"""Type hint for an object error."""

type ArrayErrorType = dict[int, ObjectErrorType]
"""Type hint for an array error."""

type _RawFieldValue = str | bytes | bytearray | memoryview
"""Type hint for a bytes field value."""

type _ReaderFieldValue = BufferedReader | IOBase | Path
"""Type hint for a reader field value."""

type FieldValueType = JsonValue | _RawFieldValue | _ReaderFieldValue


class Response(NamedTuple):
    """Response structure for the HTTP client."""

    raw_response: aiohttp.ClientResponse
    """Raw response object."""

    status: HTTPStatus
    """Response status code."""

    headers: dict[str, str]
    """Response headers."""

    raw_body: bytes
    """Raw response body."""

    # Any type is used here because it make too many typing errors when using JsonValue
    body: Any
    """Parsed response body."""


@dataclass(slots=True)
class Request:
    """Request data class.

    I want to make it simple and easy to use so I'm using dataclass
    instead of pydantic BaseModel.
    """

    method: headers.HttpMethod
    """HTTP method to use."""

    url: StrOrURL
    """URL to send the request to."""

    payload: JsonValue | FormPayload | None = None
    """Payload to send with the request."""

    headers: dict[str, str] = field(default_factory=dict)
    """Headers to send with the request."""


class FormPayload:
    """Form data class."""

    def __init__(self, fields: dict[str, FormField] | None = None) -> None:
        """Initialize the form data.

        Args:
            fields: Fields to initialize the form with.
        """
        self._fields: dict[str, FormField] = fields or {}

    def __iter__(self) -> Iterator[tuple[str, FormField]]:
        """Iterate over the form fields."""
        yield from ((name, field) for name, field in self._fields.items())

    def __len__(self) -> int:  # pragma: no cover
        """Return the number of fields in the form data."""
        return len(self._fields)


@dataclass(slots=True, frozen=True)
class FormField:
    """Form field data class."""

    value: FieldValueType
    """Field value."""

    content_type: str | None = None
    """Content type of the file."""

    filename: str | None = None
    """Name of the file."""

    def serialize(self) -> FieldValueType:
        """Serialize field value."""
        return self.value


@dataclass(slots=True, frozen=True)
class JsonField(FormField):
    """Json field data class."""

    value: JsonValue
    """Field value."""

    content_type: str | None = headers.JSON_CONTENT_TYPE
    """Content type of the file."""

    def serialize(self) -> str:
        """Serialize field value to JSON string."""
        return json.dumps(self.value)


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
