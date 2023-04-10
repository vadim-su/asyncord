"""Interfaces for the async HTTP client."""

from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO, Protocol, AsyncContextManager
from collections.abc import Sequence

from asyncord.typedefs import StrOrURL

if TYPE_CHECKING:
    from typing import Any
    from collections.abc import Mapping

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


class AsyncHttpClientPort(AsyncContextManager, Protocol):  # noqa: WPS214 - Found too many methods
    """Interface for the async HTTP client."""

    async def get(
        self,
        url: StrOrURL,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def post(
        self,
        url: StrOrURL,
        payload: Any,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def put(
        self,
        url: StrOrURL,
        payload: Any,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def patch(
        self,
        url: StrOrURL,
        payload: Any,
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    async def delete(
        self,
        url: StrOrURL,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        ...

    def set_headers(self, headers: Mapping[str, str]) -> None:
        ...

    def start(self) -> None:
        ...

    async def close(self) -> None:
        ...
