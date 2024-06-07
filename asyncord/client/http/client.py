"""Base asyncronous HTTP client."""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, NamedTuple

import aiohttp
from aiohttp.client import ClientResponse

from asyncord.client.http.headers import JSON_CONTENT_TYPE, HttpMethod
from asyncord.client.http.middleware import AttachedFile, BaseMiddleware
from asyncord.typedefs import Payload, StrOrURL

logger = logging.getLogger(__name__)


class HttpClient:
    """Asyncronous HTTP client."""

    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        middlewares: list[BaseMiddleware] | None = None,
    ) -> None:
        """Initialize the client."""
        asyncio.get_running_loop()
        self._session = session
        self.middlewares = middlewares or []
        self.system_middlewares = []

    async def get(
        self,
        *,
        url: StrOrURL,
        headers: Mapping[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a GET request.

        Args:
            url: URL to send the request to.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response response from the request.
        """
        return await self.request(
            Request(
                method=HttpMethod.GET,
                url=url,
                headers=headers,
            ),
            skip_middleware=skip_middleware,
        )

    async def post(
        self,
        *,
        url: StrOrURL,
        payload: Payload,
        files: list[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a POST request.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response from the request.
        """
        return await self.request(
            Request(
                method=HttpMethod.POST,
                url=url,
                payload=payload,
                files=files,
                headers=headers,
            ),
            skip_middleware=skip_middleware,
        )

    async def put(
        self,
        *,
        url: StrOrURL,
        payload: Payload,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a PUT request.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response from the request.
        """
        return await self.request(
            Request(
                method=HttpMethod.PUT,
                url=url,
                payload=payload,
                files=files,
                headers=headers,
            ),
            skip_middleware=skip_middleware,
        )

    async def patch(
        self,
        *,
        url: StrOrURL,
        payload: Payload,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a PATCH request.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response from the request.
        """
        return await self.request(
            Request(
                method=HttpMethod.PATCH,
                url=url,
                payload=payload,
                files=files,
                headers=headers,
            ),
            skip_middleware=skip_middleware,
        )

    async def delete(
        self,
        *,
        url: StrOrURL,
        payload: Payload | None = None,
        headers: Mapping[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a DELETE request.

        Args:
            url: Url to send the request to.
            payload: Payload to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Response:
            Response from the request.
        """
        return await self.request(
            Request(
                method=HttpMethod.DELETE,
                url=url,
                payload=payload,
                headers=headers,
            ),
            skip_middleware=skip_middleware,
        )

    async def request(self, request: Request, *, skip_middleware: bool = False) -> Response:
        """Make a request to the Discord API.

        Args:
            request: Request data.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response from the request.

        Raises:
            ClientError: If the response status code is in the 400 range.
            ServerError: If the response status code is in the 500 range.
            RateLimitError: If the response status code is 429 and the retry_after is greater than 10.
        """
        return await self.middleware.handle(
            request_data=request,
            http_client=self,
        )

    async def _raw_request(self, request_data: Request) -> Response:
        """Make a raw http request.

        When files are provided, the payload is sent as a form.

        Reference:
        https://discord.com/developers/docs/resources/channel#create-message.

        Args:
            request_data: Request data.

        Returns:
            Response context.
        """
        data = None

        if request_data.files:
            data = aiohttp.FormData()
            if request_data.payload is not None:
                data.add_field('payload_json', json.dumps(request_data.payload), content_type=JSON_CONTENT_TYPE)

            for index, (file_name, content_type, file_data) in enumerate(request_data.files):
                data.add_field(f'files[{index}]', file_data, filename=file_name, content_type=content_type)

        elif request_data.payload is not None:
            data = aiohttp.JsonPayload(request_data.payload)

        if self._session:
            req_context = self._session.request(
                request_data.method,
                request_data.url,
                data=data,
                headers=request_data.headers,
            )
        req_context = aiohttp.request(
            request_data.method,
            request_data.url,
            data=data,
            headers=request_data.headers,
        )

        async with req_context as resp:
            return Response(
                status=resp.status,
                headers=resp.headers,
                raw_body=await resp.text(),
                body=await self._extract_body(resp),
            )

    @classmethod
    async def _extract_body(cls, resp: ClientResponse) -> dict[str, Any]:
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
                return {}

        return {}


class Response(NamedTuple):
    """Response structure for the HTTP client."""

    status: int
    """Response status code."""

    headers: Mapping[str, str]
    """Response headers."""

    raw_body: Any
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

    payload: Any | None = (None,)
    """Payload to send with the request."""

    files: Sequence[AttachedFile] | None = None
    """Files to send with the request."""

    headers: Mapping[str, str] | None = None
    """Headers to send with the request."""
