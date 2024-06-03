"""This module contains the Proxy class.

This class controls the incoming calls to http_client.
And handles the limits with strategy.
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from http import HTTPStatus
from types import MappingProxyType
from typing import Any, BinaryIO, NamedTuple

from aiohttp import ClientResponse
from pydantic import BaseModel, Field

from asyncord.client.http import errors
from asyncord.client.http.bucket_track import Bucket, BucketTrack
from asyncord.client.http.headers import JSON_CONTENT_TYPE, HttpMethod
from asyncord.typedefs import StrOrURL

logger = logging.getLogger(__name__)


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


class Response(NamedTuple):
    """Response structure for the HTTP client."""

    status: int
    """Response status code."""

    headers: Mapping[str, str]
    """Response headers."""

    body: Any
    """Response body."""


class RateLimitBody(BaseModel):
    """The body of a rate limit response."""

    message: str
    """Message saying you are being rate limited."""

    retry_after: float
    """Number of seconds to wait before submitting another request."""

    is_global: bool = Field(alias='global')
    """Whether this is a global rate limit."""


@dataclass
class RequestData:
    """Request data class."""

    method: HttpMethod
    """HTTP method to use."""

    url: StrOrURL
    """URL to send the request to."""

    payload: Any | None = (None,)
    """Payload to send with the request."""

    files: Sequence[AttachedFile] | None = None
    """Files to send with the request."""

    headers: Mapping[str, str] | None = None
    """Headers to send with the request."""


class MiddleWare(ABC):
    """Middleware template."""

    @abstractmethod
    async def before_request(
        self,
        request_data: RequestData,
    ) -> RequestData:
        """Pre request rate limit handling."""

    @abstractmethod
    async def after_request(self, response: ClientResponse) -> Response:
        """After request rate limit handling."""
        ...


class BasicMiddleWare(MiddleWare):
    """Basic Middleware.

    It's basic cause I have no idea what it's supposed to do yet.
    """

    def __init__(
        self,
        headers: Mapping[str, str] | None,
        bucket_tracker: BucketTrack | None = None,
    ) -> None:
        """Initialize the middleware.

        Args:
            headers: Headers to send with the request. Defaults to None.
            bucket_tracker: Bucket tracker. Defaults to None.
        """
        self._headers = headers or {}
        self._bucket_tracker = bucket_tracker or BucketTrack()

    async def before_request(
        self,
        request_data: RequestData,
    ) -> RequestData:
        """Pre request middleware checks."""
        if self._headers:
            request_data.headers = {**self._headers, **(request_data.headers or {})}
        return request_data

    async def after_request(
        self,
        request_data: RequestData,
        response: ClientResponse,
    ) -> Response:
        """Post request middleware checks."""
        # Implement your custom rate limit handling logic here.
        body = await self._extract_body(response)
        status = response.status

        self._update_buckets(response)

        if response.status < HTTPStatus.BAD_REQUEST:
            return Response(
                status=response.status,
                headers=MappingProxyType(dict(response.headers.items())),
                body=body,
            )

        if not isinstance(body, dict):
            raise errors.ServerError(
                message='Expected JSON body',
                payload=request_data.payload,
                headers=request_data.headers,
                resp=response,
                body=body,
            )

        if status == HTTPStatus.TOO_MANY_REQUESTS:
            # FIXME: It's a simple hack for now. Potentially 'endless' recursion
            ratelimit = RateLimitBody.model_validate(body)
            logger.warning('Rate limited: %s (retry after %s)', ratelimit.message, ratelimit.retry_after)

            max_retry = 5

            if ratelimit.retry_after > max_retry:
                raise errors.RateLimitError(
                    message=ratelimit.message,
                    payload=request_data.payload,
                    headers=request_data.headers,
                    resp=response,
                    retry_after=ratelimit.retry_after,
                )

        error_body = errors.RequestErrorBody.model_validate(body)

        if status == HTTPStatus.NOT_FOUND:
            raise errors.NotFoundError(
                message=body.get('message', 'Unknown'),
                payload=request_data.payload,
                headers=request_data.headers,
                resp=response,
                body=error_body,
            )

        if HTTPStatus.BAD_REQUEST <= status < HTTPStatus.INTERNAL_SERVER_ERROR:
            raise errors.ClientError(
                message=error_body.message,
                payload=request_data.payload,
                headers=request_data.headers,
                resp=response,
                body=error_body,
            )

        raise errors.ServerError(
            message=error_body.message,
            payload=request_data.payload,
            headers=request_data.headers,
            resp=response,
            body=error_body,
        )

    @classmethod
    async def _extract_body(cls, resp: ClientResponse) -> dict[str, Any] | str:
        """Extract the body from the response.

        Args:
            resp: Request response.

        Returns:
            Body of the response.
        """
        if resp.status == HTTPStatus.NO_CONTENT:
            return {}

        if resp.headers.get('Content-Type') == JSON_CONTENT_TYPE:
            try:
                return await resp.json()
            except json.JSONDecodeError:
                body = await resp.text()
                logger.warning('Failed to decode JSON body: %s', body)
                if body:
                    return body
                return {}

        return {}

    def _update_buckets(self, response: ClientResponse) -> None:
        """Update the bucket tracker."""
        bucket_name = response.headers.get('X-RateLimit-Bucket')

        if not bucket_name:
            return

        bucket = Bucket(
            name=bucket_name,
            count=int(response.headers.get('X-RateLimit-Remaining', 0)),
            reset=float(response.headers.get('X-RateLimit-Reset-After', 0)),
            limit=int(response.headers.get('X-RateLimit-Limit', 0)),
        )

        self._bucket_tracker.increment(bucket)
