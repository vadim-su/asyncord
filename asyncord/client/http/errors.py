from __future__ import annotations

from typing import Any, Mapping

from aiohttp import ClientResponse
from pydantic import BaseModel


class BaseDiscordError(Exception):
    """Base class for all Discord errors."""

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class DiscordHTTPError(BaseDiscordError):
    """Base class for all Discord HTTP errors."""

    def __init__(
        self,
        message: str,
        payload: Any,
        headers: Mapping[str, str],
        resp: ClientResponse,
    ) -> None:
        super().__init__(message)
        self.payload = payload
        self.headers = headers
        self.resp = resp
        self.status = resp.status

    def __str__(self) -> str:
        if self.resp.reason:
            return "HTTP {0.status} ({0.reason}): {1}".format(self.resp, self.message)
        return "HTTP {0.status}: {1}".format(self.resp, self.message)


class ClientError(DiscordHTTPError):
    """Error raised when the client encounters an error.

    Usually this is due to a bad request (4xx).
    """

    def __init__(
        self,
        message: str,
        payload: Any,
        headers: Mapping[str, str],
        resp: ClientResponse,
        body: RequestErrorBody,
    ) -> None:
        """Initialize the ClientError.

        Args:
            message (str): The error message.
            payload (Any): The payload of the request.
            headers (Mapping[str, str]): The headers of the request.
            resp (ClientResponse): The response of the request.
            body (RequestErrorBody): The body of the request.
        """
        super().__init__(message, payload, headers, resp)
        self.body = body

    def __str__(self) -> str:
        """Format the error."""
        if self.resp.reason:
            exc_str = 'HTTP {0.status} ({0.reason})'.format(self.resp)
        else:
            exc_str = 'HTTP {0.status}'.format(self.resp)

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
            path (str): Path to the error block.
            errors (ErrorBlock | ObjectErrorType | ArrayErrorType): The error block to get the errors from.

        Returns:
            list[ErrorItem]: The errors.
        """
        if isinstance(errors, ErrorBlock):
            return path + '\n'.join(f'\t-> {error.code}: {error.message}' for error in errors._errors)

        return '\n'.join(self._format_errors(f'{path}.{key}', value) for key, value in errors.items())


class RateLimitError(DiscordHTTPError):
    """Error raised when the client encounters a rate limit.

    This is usually due to too many requests (429).
    """

    def __init__(
        self,
        message: str,
        payload: Any,
        headers: Mapping[str, str],
        resp: ClientResponse,
        retry_after: float,
    ) -> None:
        super().__init__(message, payload, headers, resp)
        self.retry_after = retry_after

    def __str__(self) -> str:
        return f'{self.message} (retry after {self.retry_after})'


class ServerError(DiscordHTTPError):
    """Error raised when the server return status code >= 500."""

    def __init__(
        self,
        message: str,
        payload: Any,
        headers: Mapping[str, str],
        resp: ClientResponse,
        body: RequestErrorBody | str | None = None,
    ) -> None:
        """Initialize the ServerError.

        Args:
            message (str): The error message.
            payload (Any): The payload of the request.
            headers (Mapping[str, str]): The headers of the request.
            resp (ClientResponse): The response of the request.
            body (RequestErrorBody): The body of the request.
        """
        super().__init__(message, payload, headers, resp)
        self.body = body

    def __str__(self) -> str:
        """Format the error."""
        if self.resp.reason:
            exc_str = 'HTTP {0.status} ({0.reason})'.format(self.resp)
        else:
            exc_str = 'HTTP {0.status}'.format(self.resp)

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
            path (str): Path to the error block.
            errors (ErrorBlock | ObjectErrorType | ArrayErrorType): The error block to get the errors from.

        Returns:
            list[ErrorItem]: The errors.
        """
        if isinstance(errors, ErrorBlock):
            return path + '\n'.join(f'\t-> {error.code}: {error.message}' for error in errors._errors)

        return '\n'.join(self._format_errors(f'{path}.{key}', value) for key, value in errors.items())


class ErrorItem(BaseModel):
    """Represents an error item."""

    code: int
    """Error code."""

    message: str
    """Error message."""


class ErrorBlock(BaseModel):
    """Represents an object error."""

    _errors: list[ErrorItem]
    """List of errors."""


type ObjectErrorType = dict[str, ErrorBlock | ObjectErrorType | ArrayErrorType]
"""Type hint for an object error."""

type ArrayErrorType = dict[int, ObjectErrorType]
"""Type hint for an array error."""


class RequestErrorBody(BaseModel):
    """Represents a body of a request error."""

    code: int
    """Error code."""

    message: str
    """Error message."""

    errors: ErrorBlock | ObjectErrorType | None = None
