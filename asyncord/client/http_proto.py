from __future__ import annotations

import typing

from asyncord.typedefs import StrOrURL


class Response(typing.Protocol):
    status: int
    headers: typing.Mapping[str, str]
    body: typing.Any


class AsyncHttpClientPort(typing.AsyncContextManager, typing.Protocol):
    async def get(
        self,
        url: StrOrURL,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def post(
        self,
        url: StrOrURL,
        payload: typing.Any,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def put(
        self,
        url: StrOrURL,
        payload: typing.Any,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def patch(
        self,
        url: StrOrURL,
        payload: typing.Any,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def delete(
        self,
        url: StrOrURL,
        payload: typing.Any | None = None,
        headers: typing.Mapping[str, str] | None = None,
    ) -> Response:
        ...

    def set_headers(self, headers: typing.Mapping[str, str]) -> None:
        ...

    def start(self) -> None:
        ...

    async def close(self) -> None:
        ...
