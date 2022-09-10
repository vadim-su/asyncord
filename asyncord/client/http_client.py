from __future__ import annotations

import typing
import asyncio
import logging
from http import HTTPStatus
from types import MappingProxyType
from dataclasses import dataclass

import aiohttp

from asyncord.typedefs import StrOrURL
from asyncord.client.headers import HttpMethod

logging.basicConfig(level=logging.DEBUG)


class Response(typing.NamedTuple):
    status: int
    headers: typing.Mapping[str, str]
    body: typing.Any


@dataclass
class FieldError:
    code: str
    message: str


class DiscordError(Exception):
    def __init__(
        self,
        message: str,
        code: int,
        field_errors: dict[str, list[FieldError]] | None = None,
    ) -> None:
        field_errors_message = ''
        if field_errors:
            for field, errors in field_errors.items():
                field_errors_message += '\n'
                field_errors_message += f'{field}: '
                field_errors_message += '\n\t'.join(
                    [f'{error.code} - {error.message}' for error in errors],
                )
        exc_message = f'({code}) {message}{field_errors_message}'

        super().__init__(exc_message)
        self.message = message
        self.code = code
        self.field_errors = field_errors


class AsyncHttpClient:
    def __init__(self) -> None:
        asyncio.get_running_loop()
        self._session: aiohttp.ClientSession | None = None
        self._headers = {}

    async def get(
        self,
        url: StrOrURL,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        return await self._request(HttpMethod.GET, url, headers)

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
    ):
        if headers is None:
            headers = self._headers
        else:
            headers = {**self._headers, **headers}

        if self._session:
            resp_context = self._session.request(method, url, json=payload, headers=headers)
        else:
            resp_context = aiohttp.request(method, url, json=payload, headers=headers)

        async with resp_context as resp:
            if resp.status == HTTPStatus.NO_CONTENT:
                body = {}
            else:
                body = await resp.json()

            if resp.status >= HTTPStatus.BAD_REQUEST:
                # field_errors = {}
                # if body.get('errors'):
                #     for field, errors in body['errors']:
                #         field_errors[field] = [
                #             FieldError(error['code'], error['message'])
                #             for error in errors['_errors']
                #         ]

                # TODO: This is a client error, not a server error which is a 500, need to handle this better
                raise DiscordError(message=body['message'], code=body['code'])

            return Response(
                status=resp.status,
                headers=MappingProxyType(dict(resp.headers.items())),
                body=body,
            )
