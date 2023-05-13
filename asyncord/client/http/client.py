"""Base asyncronous HTTP client."""

from __future__ import annotations

import json
import asyncio
import logging
from http import HTTPStatus
from types import MappingProxyType
from typing import TYPE_CHECKING, BinaryIO, NamedTuple
from collections.abc import Mapping, Sequence

import aiohttp
from pydantic import Field, BaseModel
from rich.logging import RichHandler
from aiohttp.client import ClientResponse

from asyncord.typedefs import StrOrURL
from asyncord.client.http import errors
from asyncord.client.http.headers import JSON_CONTENT_TYPE, HttpMethod

if TYPE_CHECKING:
    from typing import Any, Self, AsyncContextManager

logging.basicConfig(
    handlers=[
        RichHandler(
            omit_repeated_times=False,
            rich_tracebacks=True,
        ),
    ],
    level=logging.DEBUG,
)


AttachedFile = tuple[str, str, BinaryIO | bytes]
"""Type alias for a file to be attached to a request.

The tuple contains the filename, the content type, and the file object.
"""


class Response(NamedTuple):
    """Response structure for the HTTP client."""

    status: int
    headers: Mapping[str, str]
    body: Any


class RateLimitBody(BaseModel):
    """The body of a rate limit response."""

    message: str
    """Message saying you are being rate limited."""

    retry_after: float
    """Number of seconds to wait before submitting another request."""

    global_: bool = Field(alias='global')
    """Whether this is a global rate limit."""


class AsyncHttpClient:  # noqa: WPS214 - Found too many methods
    """Asyncronous HTTP client."""

    def __init__(self) -> None:
        """Initialize the client."""
        asyncio.get_running_loop()
        self._session: aiohttp.ClientSession | None = None
        self._headers = {}

    async def get(
        self,
        url: StrOrURL,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a GET request.

        Args:
            url (StrOrURL): URL to send the request to.
            headers (Mapping[str, str] | None): Headers to send with the request.
                Defaults to None.

        Returns:
            Response: response from the request.
        """
        return await self._request(HttpMethod.GET, url, headers=headers)

    async def post(
        self,
        url: StrOrURL,
        payload: Any,
        files: list[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a POST request.

        Args:
            url (StrOrURL): URL to send the request to.
            payload (Any): Payload to send with the request.
            headers (Mapping[str, str] | None): Headers to send with the request.
                Defaults to None.
            send_as_form (bool): Whether to send the payload as a form. Defaults to False.

        Returns:
            Response: response from the request.
        """
        return await self._request(HttpMethod.POST, url, payload, files, headers)

    async def put(
        self,
        url: StrOrURL,
        payload: Any,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a PUT request.

        Args:
            url (StrOrURL): URL to send the request to.
            payload (Any): Payload to send with the request.
            headers (Mapping[str, str] | None):
                Headers to send with the request. Defaults to None.

        Returns:
            Response: response from the request.
        """
        return await self._request(HttpMethod.PUT, url, payload, files, headers)

    async def patch(
        self,
        url: StrOrURL,
        payload: Any,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a PATCH request.

        Args:
            url (StrOrURL):
                URL to send the request to.
            payload (Any):
                Payload to send with the request.
            headers (Mapping[str, str] | None):
                Headers to send with the request. Defaults to None.

        Returns:
            Response: Response from the request.
        """
        return await self._request(HttpMethod.PATCH, url, payload, files, headers)

    async def delete(
        self,
        url: StrOrURL,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a DELETE request.

        Args:
            url (StrOrURL):
                Url to send the request to.
            payload (Any | None):
                Payload to send with the request. Defaults to None.
            headers (Mapping[str, str] | None):
                Headers to send with the request. Defaults to None.

        Returns:
            Response: Response from the request.
        """
        return await self._request(HttpMethod.DELETE, url, payload, headers=headers)

    def set_headers(self, headers: Mapping[str, str]) -> None:
        """Set the headers to send with requests.

        Args:
            headers (Mapping[str, str]): Headers to send with requests.
        """
        # FIXME: #3 session can be used outside of the current client and we shouldn't be setting it here
        self._headers = headers
        if self._session:
            self._session.headers.clear()
            self._session.headers.update(headers)

    def start(self) -> None:
        """Initialize the client."""
        asyncio.get_running_loop()
        self._session = aiohttp.ClientSession()
        self.set_headers(self._headers)

    async def close(self) -> None:
        """Close the client."""
        if self._session:
            await self._session.close()

    async def __aenter__(self) -> Self:
        """Initialize the client when used as a context manager.

        Returns:
            Self: Initialized client.
        """
        self.start()
        return self

    async def __aexit__(self, _exc_type, _exc, _tb):
        """Close the client when used as a context manager."""
        await self.close()

    async def _request(
        self,
        method: HttpMethod,
        url: StrOrURL,
        payload: Any | None = None,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Make a request to the Discord API.

        Args:
            method (HttpMethod): HTTP method to use.
            url (StrOrURL): Url to request.
            payload (Any, optional): Payload to send. Defaults to None.
            headers (Mapping[str, str], optional): Headers to send. Defaults to None.
            send_as_form (bool): Whether to send the payload as a form. Defaults to False.

        Returns:
            Response: Response from the request.

        Raises:
            ClientError: If the response status code is in the 400 range.
            ServerError: If the response status code is in the 500 range.
            RateLimitError: If the response status code is 429 and
                the retry_after is greater than 10.
        """
        if headers is None:
            headers = self._headers
        else:
            headers = {**self._headers, **headers}
        logging.basicConfig(level=logging.DEBUG)

        async with self._make_raw_request(method, url, payload, files, headers) as resp:
            body, message = await self._extract_body_and_message(resp)

            match resp.status:
                case status if status < HTTPStatus.BAD_REQUEST:
                    return Response(
                        status=resp.status,
                        headers=MappingProxyType(dict(resp.headers.items())),
                        body=body,
                    )

                case HTTPStatus.TOO_MANY_REQUESTS:
                    # FIXME: It's a simple hack for now. Potentially 'endless' recursion
                    ratelimit = RateLimitBody(**body)
                    if ratelimit.retry_after > 10:
                        raise errors.RateLimitError(  # noqa: WPS220 - Found too deep nesting
                            message=message or 'Unknown error',
                            resp=resp,
                            retry_after=ratelimit.retry_after or None,
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

                case status if HTTPStatus.BAD_REQUEST <= status < HTTPStatus.INTERNAL_SERVER_ERROR:
                    # TODO: #8 Add more specific errors for 400 range
                    raise errors.ClientError(
                        message=message or 'Unknown error',
                        resp=resp,
                        code=body.get('code'),
                    )

                case _:
                    raise errors.ServerError(
                        message=message or 'Unknown error',
                        resp=resp,
                        status_code=resp.status,
                    )

    async def _extract_body_and_message(self, resp: ClientResponse) -> tuple[Any, str | None]:
        """Extract the body and message from the response.

        Args:
            resp (ClientResponse): request response.

        Returns:
            tuple[Any, str | None]: body and message from the response.
        """
        if resp.status == HTTPStatus.NO_CONTENT:
            body = {}
            message = None
        elif resp.headers.get('Content-Type') == JSON_CONTENT_TYPE:
            body = await resp.json()
            message = body.get('message') if isinstance(body, Mapping) else None
        else:
            body = {}
            message = await resp.text()

        return body, message

    def _make_raw_request(
        self,
        method: HttpMethod,
        url: StrOrURL,
        payload: Any | None = None,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> AsyncContextManager[ClientResponse]:
        """Make a raw http request.

        When files are provided, the payload is sent as a form.
        Read more here: https://discord.com/developers/docs/resources/channel#create-message.

        Args:
            method(HttpMethod): The HTTP method to use.
            url(StrOrURL): The URL to request.
            payload(Optional[Any]): The payload to send. Defaults to None.
            files(Optional[Sequence[AttachedFile]]): The files to send. Defaults to None.
            headers(Optional[Mapping[str, str]]): The headers to send. Defaults to None.

        Returns:
            AsyncContextManager[ClientResponse]: The response context.
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
        else:
            return aiohttp.request(method, url, data=data, headers=headers)
