from __future__ import annotations

import typing

from asyncord.typedefs import StrOrURL


class Response(typing.Protocol):
    op: int
    d: typing.Any
    s: int
    t: str
    _trace: typing.Optional[typing.Any] = None


class AsyncWSClientPort(typing.AsyncContextManager, typing.Protocol):
    async def connect(self, url: StrOrURL) -> None:
        ...

    def start(self) -> None:
        ...

    async def close(self) -> None:
        ...
