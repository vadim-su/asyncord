"""This module contains all the errors that can be raised by the HTTP client."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from aiohttp import ClientResponse
from pydantic import BaseModel, Field

from asyncord.client.http.error_codes import ErrorCode


class BaseDiscordError(Exception):
    """Base class for all Discord errors."""

    def __init__(self, message: str) -> None:
        """Initialize the BaseDiscordError."""
        self.message = message

    def __str__(self) -> str:
        """Format the error."""
        return self.message


class DiscordHTTPError(BaseDiscordError):
    """Base class for all Discord HTTP errors."""

    def __init__(
        self,
        message: str,
        payload: Any,  # noqa: ANN401
        headers: Mapping[str, str],
        resp: ClientResponse,
    ) -> None:
        """Initialize the DiscordHTTPError.

        Args:
            message: The error message.
            payload: The payload of the request.
            headers: The headers of the request.
            resp: The response of the request.
        """
        super().__init__(message)
        self.payload = payload
        self.headers = headers
        self.resp = resp
        self.status = resp.status

    def __str__(self) -> str:
        """Format the error."""
        if self.resp.reason:
            return f'HTTP {self.resp.status} ({self.resp.reason}): {self.message}'
        return f'HTTP {self.resp.status}: {self.message}'


class ClientError(DiscordHTTPError):
    """Error raised when the client encounters an error.

    Usually this is due to a bad request (4xx).
    """

    def __init__(  # noqa: PLR0913
        self,
        *,
        message: str,
        payload: Any,  # noqa: ANN401
        headers: Mapping[str, str],
        resp: ClientResponse,
        body: RequestErrorBody,
    ) -> None:
        """Initialize the ClientError.

        Args:
            message: The error message.
            payload: The payload of the request.
            headers: The headers of the request.
            resp: The response of the request.
            body: The body of the request.
        """
        super().__init__(message, payload, headers, resp)
        self.body = body

    def __str__(self) -> str:
        """Format the error."""
        if self.resp.reason:
            exc_str = f'HTTP {self.resp.status} ({self.resp.reason})'
        else:
            exc_str = f'HTTP {self.resp.status}'

        if not self.body:
            return exc_str

        if isinstance(self.body, str):
            return f'{exc_str}\n{self.body}'

        exc_str = f'{exc_str}\nCode {self.body.code}: {self.body.message}'
        if not self.body.errors:
            return exc_str

        return f'{exc_str}\n' + self._format_errors('', self.body.errors)

    def _format_errors(self, path: str, errors: ErrorBlock | ObjectErrorType | ArrayErrorType) -> str:
        """Get all errors from an error block.

        Args:
            path: Path to the error block.
            errors: The error block to get the errors from.

        Returns:
            String representation of the errors.
        """
        if isinstance(errors, ErrorBlock):
            return path + '\n'.join(f'\t-> {error.code}: {error.message}' for error in errors.errors)

        error_item_str_list = []

        for field_name, error in errors.items():
            if path:
                new_path = f'{path}.{field_name}'
            else:
                new_path = str(field_name)

            error_item_str_list.append(self._format_errors(new_path, error))

        return '\n'.join(error_item_str_list)


class NotFoundError(ClientError):
    """Error raised when status code 404 occurs."""


class RateLimitError(DiscordHTTPError):
    """Error raised when the client encounters a rate limit.

    This is usually due to too many requests (429).
    """

    def __init__(  # noqa: PLR0913
        self,
        *,
        message: str,
        payload: Any,  # noqa: ANN401
        headers: Mapping[str, str],
        resp: ClientResponse,
        retry_after: float,
    ) -> None:
        """Initialize the RateLimitError.

        Args:
            message: The error message.
            payload: The payload of the request.
            headers: The headers of the request.
            resp: The response of the request.
            retry_after: The time in seconds until the client can make another request.
        """
        super().__init__(message, payload, headers, resp)
        self.retry_after = retry_after

    def __str__(self) -> str:
        """Format the error."""
        return f'{self.message} (retry after {self.retry_after})'


class ServerError(DiscordHTTPError):
    """Error raised when the server return status code >= 500."""

    def __init__(  # noqa: PLR0913
        self,
        *,
        message: str,
        payload: Any,  # noqa: ANN401
        headers: Mapping[str, str],
        resp: ClientResponse,
        body: RequestErrorBody | str | None = None,
    ) -> None:
        """Initialize the ServerError.

        Args:
            message: The error message.
            payload: The payload of the request.
            headers: The headers of the request.
            resp: The response of the request.
            body: The body of the request.
        """
        super().__init__(message, payload, headers, resp)
        self.body = body

    def __str__(self) -> str:
        """Format the error."""
        if self.resp.reason:
            exc_str = f'HTTP {self.resp.status} ({self.resp.reason})'
        else:
            exc_str = f'HTTP {self.resp.status}'

        if not self.body:
            return exc_str

        if isinstance(self.body, str):
            return f'{exc_str}\n{self.body}'

        exc_str = f'{exc_str} - {self.body.code}: {self.body.message}'
        if not self.body.errors:
            return exc_str

        return f'{exc_str}\n' + self._format_errors('', self.body.errors)

    def _format_errors(self, path: str, errors: ErrorBlock | ObjectErrorType | ArrayErrorType) -> str:
        """Get all errors from an error block.

        Args:
            path: Path to the error block.
            errors: The error block to get the errors from.

        Returns:
            String representation of the errors.
        """
        if isinstance(errors, ErrorBlock):
            return path + '\n'.join(f'\t-> {error.code}: {error.message}' for error in errors.errors)

        error_item_str_list = []

        for field_name, error in errors.items():
            if path:
                new_path = f'{path}.{field_name}'
            else:
                new_path = str(field_name)

            error_item_str_list.append(self._format_errors(new_path, error))

        return '\n'.join(error_item_str_list)


class ErrorItem(BaseModel):
    """Represents an error item."""

    code: str
    """Error code."""

    message: str
    """Error message."""


class ErrorBlock(BaseModel):
    """Represents an object error."""

    errors: list[ErrorItem] = Field(alias='_errors')
    """List of errors."""


type ObjectErrorType = dict[str, ErrorBlock | ObjectErrorType | ArrayErrorType]
"""Type hint for an object error."""

type ArrayErrorType = dict[int, ObjectErrorType]
"""Type hint for an array error."""


class RequestErrorBody(BaseModel):
    """Represents a body of a request error."""

    code: ErrorCode
    """Error code."""

    message: str
    """Error message."""

    errors: ErrorBlock | ObjectErrorType | None = None
    """Error block."""
