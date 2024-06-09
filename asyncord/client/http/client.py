"""Base asyncronous HTTP client."""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Sequence
from functools import partial
from http import HTTPStatus
from typing import Any

import aiohttp
from aiohttp.client import ClientResponse

from asyncord.client.http.headers import JSON_CONTENT_TYPE, HttpMethod
from asyncord.client.http.middleware.base import Middleware, NextCallType
from asyncord.client.http.middleware.errors import ErrorHandlerMiddleware
from asyncord.client.http.models import AttachedFile, Request, Response
from asyncord.typedefs import StrOrURL

logger = logging.getLogger(__name__)


class HttpClient:
    """Asyncronous HTTP client."""

    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        middlewares: list[Middleware] | None = None,
    ) -> None:
        """Initialize the client.

        Args:
            session: Client session. Defaults to None.
            middlewares: Middlewares to apply. Defaults to None.
        """
        asyncio.get_running_loop()  # we want to make sure we are running in an event loop
        self.session = session
        self.middlewares: list[Middleware] = middlewares or []
        self.system_middlewares: list[Middleware] = [ErrorHandlerMiddleware()]

    async def get(
        self,
        *,
        url: StrOrURL,
        headers: dict[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a GET request.

        Args:
            url: URL to send the request to.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.GET,
                url=url,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    async def post(
        self,
        *,
        url: StrOrURL,
        payload: Any | None = None,  # noqa: ANN401
        files: list[AttachedFile] | None = None,
        headers: dict[str, str] | None = None,
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
            Response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.POST,
                url=url,
                payload=payload,
                files=files,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    async def put(
        self,
        *,
        url: StrOrURL,
        payload: Any | None = None,  # noqa: ANN401
        files: Sequence[AttachedFile] | None = None,
        headers: dict[str, str] | None = None,
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
            Response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.PUT,
                url=url,
                payload=payload,
                files=files,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    async def patch(
        self,
        *,
        url: StrOrURL,
        payload: Any,  # noqa: ANN401
        files: Sequence[AttachedFile] | None = None,
        headers: dict[str, str] | None = None,
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
            Response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.PATCH,
                url=url,
                payload=payload,
                files=files,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    async def delete(
        self,
        *,
        url: StrOrURL,
        payload: Any | None = None,  # noqa: ANN401
        headers: dict[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a DELETE request.

        Args:
            url: Url to send the request to.
            payload: Payload to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Response:
            Response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.DELETE,
                url=url,
                payload=payload,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    def add_middleware(self, middleware: Middleware) -> None:
        """Add a middleware to the client.

        Args:
            middleware: Middleware to add.
        """
        self.middlewares.append(middleware)

    async def request(self, request: Request, *, skip_middleware: bool = False) -> Response:
        """Make a request to the Discord API.

        Args:
            request: Request data.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response from the processed request.

        Raises:
            ClientError: If the response status code is in the 400 range.
            ServerError: If the response status code is in the 500 range.
            RateLimitError: If the response status code is 429 and the retry_after is greater than 10.
        """
        if skip_middleware:
            return await self._raw_request(request)

        return await self._apply_middleware(request)

    async def _raw_request(self, request: Request) -> Response:
        """Make a raw http request.

        When files are provided, the payload is sent as a form.

        Reference:
        https://discord.com/developers/docs/resources/channel#create-message.

        Args:
            request: Request data.

        Returns:
            Response from the processed request.
        """
        data = None

        if request.files:
            data = aiohttp.FormData()
            if request.payload is not None:
                data.add_field('payload_json', json.dumps(request.payload), content_type=JSON_CONTENT_TYPE)

            for index, (file_name, content_type, file_data) in enumerate(request.files):
                data.add_field(f'files[{index}]', file_data, filename=file_name, content_type=content_type)

        elif request.payload is not None:
            data = aiohttp.JsonPayload(request.payload)

        if self.session:
            req_context = self.session.request(
                method=request.method,
                url=request.url,
                data=data,
                headers=request.headers,
            )
        else:
            req_context = aiohttp.request(
                method=request.method,
                url=request.url,
                data=data,
                headers=request.headers,
            )

        async with req_context as resp:
            # fmt: off
            headers = {
                header.lower(): value
                for header, value in resp.headers.items()
            }
            # fmt: on

            return Response(
                raw_response=resp,
                status=HTTPStatus(resp.status),
                headers=headers,
                raw_body=await resp.read(),
                body=await self._extract_body(resp),
            )

    @classmethod
    async def _extract_body(cls, resp: ClientResponse) -> dict[str, Any]:
        """Extract the body from the response.

        Args:
            resp: Request response.

        Returns:
            Body of the parsed response.
        """
        if resp.status == HTTPStatus.NO_CONTENT:
            return {}

        if resp.headers.get('Content-Type') == JSON_CONTENT_TYPE:
            try:
                return await resp.json()
            except json.JSONDecodeError:
                body = await resp.read()
                logger.warning('Failed to decode JSON body: %s', body[:100])
                return {}

        return {}

    async def _apply_middleware(self, request: Request) -> Response:
        """Apply middleware to the request.

        Args:
            request: Request data.

        Returns:
            Response from the processed request.
        """

        async def _raw_request_wrap(
            request: Request,
            http_client: HttpClient,
        ) -> Response:
            return await self._raw_request(request)

        middlewares = self.system_middlewares + list(reversed(self.middlewares))
        next_call: NextCallType = _raw_request_wrap

        for middleware in middlewares:
            next_call = partial(middleware, next_call=next_call)

        return await next_call(request, self)
