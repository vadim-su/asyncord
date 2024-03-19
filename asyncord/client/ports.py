"""Interfaces for the async HTTP client."""

from __future__ import annotations

from collections.abc import Sequence
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


class AsyncHttpClientPort(Protocol):
    """Interface for the async HTTP client."""

    async def get(
        self,
        url: StrOrURL,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a GET request to the given URL.

        Args:
            url: URL to send the request to.
            headers: Headers to send with the request.

        Returns:
            Response object.
        """

    async def post(
        self,
        url: StrOrURL,
        payload: Any,  # noqa: ANN401
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a POST request to the given URL.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request.
            headers: Headers to send with the request.

        Returns:
            Response object.
        """

    async def put(
        self,
        url: StrOrURL,
        payload: Any,  # noqa: ANN401
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a PUT request to the given URL.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request.
            headers: Headers to send with the request.

        Returns:
            Response object.
        """

    async def patch(
        self,
        url: StrOrURL,
        payload: Any,  # noqa: ANN401
        files: Sequence[AttachedFile] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a PATCH request to the given URL.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request.
            headers: Headers to send with the request.

        Returns:
            Response object.
        """

    async def delete(
        self,
        url: StrOrURL,
        payload: Any | None = None,  # noqa: ANN401
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send a DELETE request to the given URL.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            headers: Headers to send with the request.

        Returns:
            Response object.
        """

    def set_headers(self, headers: Mapping[str, str]) -> None:
        """Set the headers to be sent with the requests.

        Args:
            headers: Headers to set.
        """
