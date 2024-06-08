"""HTTP models for the HTTP client."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from dataclasses import dataclass, field
from typing import Any, BinaryIO, NamedTuple

import aiohttp

from asyncord.client.http.headers import HttpMethod
from asyncord.typedefs import StrOrURL


class Response(NamedTuple):
    """Response structure for the HTTP client."""

    raw_response: aiohttp.ClientResponse
    """Raw response object."""

    status: int
    """Response status code."""

    headers: Mapping[str, str]
    """Response headers."""

    raw_body: str
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
