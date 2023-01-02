from __future__ import annotations

import typing
import asyncio
import logging
from http import HTTPStatus
from types import MappingProxyType

import aiohttp
from pydantic import Field, BaseModel
from rich.logging import RichHandler
from aiohttp.client import ClientResponse

from asyncord.client import client_errors as errors
from asyncord.typedefs import StrOrURL
from asyncord.client.headers import JSON_CONTENT_TYPE, HttpMethod

logging.basicConfig(
    handlers=[
        RichHandler(
            omit_repeated_times=False,
            rich_tracebacks=True,
        ),
    ],
    level=logging.DEBUG,
)


class Response(typing.NamedTuple):
    """A response from the Discord API."""
    status: int
    headers: typing.Mapping[str, str]
    body: typing.Any


class RateLimitBody(BaseModel):
    """The body of a rate limit response."""

    message: str
    """A message saying you are being rate limited."""

    retry_after: float
    """The number of seconds to wait before submitting another request."""

    global_: bool = Field(alias='global')
    """Whether this is a global rate limit."""


class AsyncHttpClient:
    """A client for the Discord API."""

    def __init__(self) -> None:
        asyncio.get_running_loop()
        self._session: aiohttp.ClientSession | None = None
        self._headers = {}

    async def get(
        self,
        url: StrOrURL,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        return await self._request(HttpMethod.GET, url, headers=headers)

    async def post(
        self,
        url: StrOrURL,
        payload: typing.Any,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        return await self._request(HttpMethod.POST, url, payload, headers)

    async def put(
        self,
        url: StrOrURL,
        payload: typing.Any,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        return await self._request(HttpMethod.PUT, url, payload, headers)

    async def patch(
        self,
        url: StrOrURL,
        payload: typing.Any,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        return await self._request(HttpMethod.PATCH, url, payload, headers)

    async def delete(
        self,
        url: StrOrURL,
        payload: typing.Any | None = None,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        return await self._request(HttpMethod.DELETE, url, payload, headers)

    def set_headers(self, headers: typing.Mapping[str, str]) -> None:
        # FIXME: session can be used outside of the current client and we shouldn't be setting it here
        self._headers = headers
        if self._session:
            self._session.headers.clear()
            self._session.headers.update(headers)

    def start(self) -> None:
        asyncio.get_running_loop()
        self._session = aiohttp.ClientSession()
        self.set_headers(self._headers)

    async def close(self) -> None:
        if self._session:
            await self._session.close()

    async def __aenter__(self) -> AsyncHttpClient:
        self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def _request(
        self,
        method: HttpMethod,
        url: StrOrURL,
        payload: typing.Any | None = None,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        if headers is None:
            headers = self._headers
        else:
            headers = {**self._headers, **headers}

        if self._session:
            resp_context = self._session.request(method, url, json=payload, headers=headers)
        else:
            resp_context = aiohttp.request(method, url, json=payload, headers=headers)

        async with resp_context as resp:
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
                        raise errors.RateLimitError(
                            message=message or 'Unknown error',
                            resp=resp,
                            retry_after=ratelimit.retry_after or None,
                        )
                    # FIXME: Move to decorator
                    await asyncio.sleep(ratelimit.retry_after + 0.1)
                    return await self._request(method, url, payload, headers)

                case status if HTTPStatus.BAD_REQUEST <= status < HTTPStatus.INTERNAL_SERVER_ERROR:
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

    async def _extract_body_and_message(self, resp: ClientResponse):
        if resp.status == HTTPStatus.NO_CONTENT:
            body = {}
            message = None
        elif resp.headers.get('Content-Type') == JSON_CONTENT_TYPE:
            body = await resp.json()
            message = body.get('message') if isinstance(body, typing.Mapping) else None
        else:
            body = {}
            message = await resp.text()

        return body, message
