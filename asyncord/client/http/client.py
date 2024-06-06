"""Base asyncronous HTTP client."""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

import aiohttp
from aiohttp.client import ClientResponse

from asyncord.client.http.headers import JSON_CONTENT_TYPE, HttpMethod
from asyncord.client.http.middleware import AttachedFile, MiddleWare, RequestData, Response
from asyncord.typedefs import Payload, StrOrURL

if TYPE_CHECKING:
    from contextlib import AbstractAsyncContextManager


MAX_NEXT_RETRY_SEC = 10
"""Maximum number of seconds to wait before retrying a request."""

logger = logging.getLogger(__name__)


class AsyncHttpClient:
    """Asyncronous HTTP client."""

    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        middleware: MiddleWare | None = None,
    ) -> None:
        """Initialize the client."""
        asyncio.get_running_loop()
        self._session = session
        self.middleware = middleware

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
        return await self._request(
            method=HttpMethod.GET,
            url=url,
            headers=headers,
        )

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
        return await self._request(
            method=HttpMethod.POST,
            url=url,
            payload=payload,
            files=files,
            headers=headers,
        )

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
        return await self._request(
            method=HttpMethod.PUT,
            url=url,
            payload=payload,
            files=files,
            headers=headers,
        )

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
        return await self._request(
            method=HttpMethod.PATCH,
            url=url,
            payload=payload,
            files=files,
            headers=headers,
        )

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
        return await self._request(
            method=HttpMethod.DELETE,
            url=url,
            payload=payload,
            headers=headers,
        )

    async def _request(  # noqa: PLR0913
        self,
        *,
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
        headers = {**(headers or {})}

        request_data = RequestData(
            method=method,
            url=url,
            payload=payload,
            files=files,
            headers=headers,
        )

        return await self.middleware.start_middleware(
            request_data=request_data,
            http_client=self,
        )

    def _make_raw_request(
        self,
        *,
        request_data: RequestData,
    ) -> AbstractAsyncContextManager[ClientResponse]:
        """Make a raw http request.

        When files are provided, the payload is sent as a form.
        Read more here: https://discord.com/developers/docs/resources/channel#create-message.

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
            return self._session.request(
                request_data.method,
                request_data.url,
                data=data,
                headers=request_data.headers,
            )
        return aiohttp.request(
            request_data.method,
            request_data.url,
            data=data,
            headers=request_data.headers,
        )
