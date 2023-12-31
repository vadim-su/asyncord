"""Base asyncronous HTTP client."""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Mapping, Sequence
from http import HTTPStatus
from types import MappingProxyType, TracebackType
from typing import TYPE_CHECKING, Any, BinaryIO, NamedTuple

import aiohttp
from aiohttp.client import ClientResponse
from pydantic import BaseModel, Field

from asyncord.client.http import errors
from asyncord.client.http.headers import JSON_CONTENT_TYPE, HttpMethod
from asyncord.typedefs import Payload, StrOrURL

if TYPE_CHECKING:
    from contextlib import AbstractAsyncContextManager
    from typing import Self


MAX_NEXT_RETRY_SEC = 10
"""Maximum number of seconds to wait before retrying a request."""

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


class AsyncHttpClient:
    """Asyncronous HTTP client."""

    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize the client."""
        asyncio.get_running_loop()
        self._session = session
        self._headers = headers or {}

    async def get(
        self,
        url: StrOrURL,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a GET request.

        Args:
            url: URL to send the request to.
            headers: Headers to send with the request. Defaults to None.

        Returns:
            Response response from the request.
        """
        return await self._request(HttpMethod.GET, url, headers=headers)

    async def post(
        self,
        url: StrOrURL,
        payload: Payload,
        files: list[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a POST request.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.

        Returns:
            Response from the request.
        """
        return await self._request(HttpMethod.POST, url, payload, files, headers)

    async def put(
        self,
        url: StrOrURL,
        payload: Payload,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a PUT request.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.

        Returns:
            Response from the request.
        """
        return await self._request(HttpMethod.PUT, url, payload, files, headers)

    async def patch(
        self,
        url: StrOrURL,
        payload: Payload,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a PATCH request.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.

        Returns:
            Response from the request.
        """
        return await self._request(HttpMethod.PATCH, url, payload, files, headers)

    async def delete(
        self,
        url: StrOrURL,
        payload: Payload | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a DELETE request.

        Args:
            url: Url to send the request to.
            payload: Payload to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.

        Response:
            Response from the request.
        """
        return await self._request(HttpMethod.DELETE, url, payload, headers=headers)

    def set_headers(self, headers: Mapping[str, str]) -> None:
        """Set the headers to send with requests.

        Args:
            headers: Headers to send with requests.
        """
        self._headers = headers

    def start(self) -> None:
        """Initialize the client."""
        asyncio.get_running_loop()  # Ensure we are running in an event loop
        self._session = aiohttp.ClientSession()

    async def close(self) -> None:
        """Close the client."""
        if self._session:
            await self._session.close()

    async def __aenter__(self) -> Self:
        """Initialize the client when used as a context manager.

        Returns:
            Initialized client.
        """
        self.start()
        return self

    async def __aexit__(
        self, _exc_type: type[BaseException] | None, _exc: BaseException | None, _tb: TracebackType | None,
    ) -> None:
        """Close the client when used as a context manager."""
        await self.close()

    async def _request(  # noqa: PLR0913
        self,
        method: HttpMethod,
        url: StrOrURL,
        payload: Payload | None = None,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Make a request to the Discord API.

        Args:
            method: HTTP method to use.
            url: URL to send the request to.
            payload: Payload to send. Defaults to None.
            files: Files to send. Defaults to None.
            headers: Headers to send. Defaults to None.

        Returns:
            Response from the request.

        Raises:
            ClientError: If the response status code is in the 400 range.
            ServerError: If the response status code is in the 500 range.
            RateLimitError: If the response status code is 429 and the retry_after is greater than 10.
        """
        headers = {**self._headers, **(headers or {})}

        async with self._make_raw_request(method, url, payload, files, headers) as resp:
            body = await self._extract_body(resp)
            status = resp.status

            if resp.status < HTTPStatus.BAD_REQUEST:
                return Response(
                    status=resp.status,
                    headers=MappingProxyType(dict(resp.headers.items())),
                    body=body,
                )

            if not isinstance(body, dict):
                raise errors.ServerError(
                    message='Expected JSON body',
                    payload=payload,
                    headers=headers,
                    resp=resp,
                    body=body,
                )

            if status == HTTPStatus.TOO_MANY_REQUESTS:
                # FIXME: It's a simple hack for now. Potentially 'endless' recursion
                ratelimit = RateLimitBody.model_validate(body)
                logger.warning(f'Rate limited: {ratelimit.message} (retry after {ratelimit.retry_after})')

                if ratelimit.retry_after > MAX_NEXT_RETRY_SEC:
                    raise errors.RateLimitError(
                        message=ratelimit.message,
                        payload=payload,
                        headers=headers,
                        resp=resp,
                        retry_after=ratelimit.retry_after,
                    )

                # FIXME: Move to decorator
                await asyncio.sleep(ratelimit.retry_after + 0.1)
                return await self._request(
                    method=method,
                    url=url,
                    payload=payload,
                    files=files,
                    headers=headers,
                )

            error_body = errors.RequestErrorBody.model_validate(body)
            if HTTPStatus.BAD_REQUEST <= status < HTTPStatus.INTERNAL_SERVER_ERROR:
                raise errors.ClientError(
                    message=error_body.message,
                    payload=payload,
                    headers=headers,
                    resp=resp,
                    body=error_body,
                )

            raise errors.ServerError(
                message=error_body.message,
                payload=payload,
                headers=headers,
                resp=resp,
                body=error_body,
            )

    async def _extract_body(self, resp: ClientResponse) -> dict[str, Any] | str:
        """Extract the body.

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
                logger.warning(f'Failed to decode JSON body: {body}')
                if body:
                    return body
                return {}

        return {}

    def _make_raw_request(  # noqa: PLR0913
        self,
        method: HttpMethod,
        url: StrOrURL,
        payload: Any | None = None,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> AbstractAsyncContextManager[ClientResponse]:
        """Make a raw http request.

        When files are provided, the payload is sent as a form.
        Read more here: https://discord.com/developers/docs/resources/channel#create-message.

        Args:
            method: HTTP method to use.
            url: URL to request.
            payload: Payload to send. Defaults to None.
            files: Files to send. Defaults to None.
            headers: Headers to send. Defaults to None.

        Returns:
            Response context.
        """
        data = None

        if files:
            data = aiohttp.FormData()
            if payload:
                data.add_field('payload_json', json.dumps(payload), content_type=JSON_CONTENT_TYPE)

            for index, (file_name, content_type, file_data) in enumerate(files):
                data.add_field(f'files[{index}]', file_data, filename=file_name, content_type=content_type)

        elif payload:
            data = aiohttp.JsonPayload(payload)

        if self._session:
            return self._session.request(method, url, data=data, headers=headers)
        return aiohttp.request(method, url, data=data, headers=headers)
