"""Interfaces for the async HTTP client."""

from __future__ import annotations

from collections.abc import Sequence
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, BinaryIO, Protocol

from asyncord.typedefs import StrOrURL

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any

AttachedFile = tuple[str, str, BinaryIO | bytes]
"""Type alias for a file to be attached to a message.

The tuple contains the filename, the content type, and the file object.
"""


class Response(Protocol):
    """Interface for Response objects returned by the HTTP client.

    Attributes:
        status: Status code of the response.
        headers: Headers of the response.
        body: Body of the response.
    """

    status: int
    headers: Mapping[str, str]
    body: Any


class AsyncHttpClientPort(AbstractAsyncContextManager, Protocol):
    """Interface for the async HTTP client."""

    async def get(  # noqa: D102
        self,
        url: StrOrURL,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def post(  # noqa: D102
        self,
        url: StrOrURL,
        payload: Any,  # noqa: ANN401
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def put(  # noqa: D102
        self,
        url: StrOrURL,
        payload: Any,  # noqa: ANN401
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def patch(  # noqa: D102
        self,
        url: StrOrURL,
        payload: Any,  # noqa: ANN401
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def delete(  # noqa: D102
        self,
        url: StrOrURL,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    def set_headers(self, headers: Mapping[str, str]) -> None:  # noqa: D102
        ...

    def start(self) -> None:  # noqa: D102
        ...

    async def close(self) -> None:  # noqa: D102
        ...
