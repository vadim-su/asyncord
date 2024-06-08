"""This module contains all the errors that can be raised by the HTTP client."""

from __future__ import annotations

import http

from pydantic import BaseModel, Field

from asyncord.client.http.error_codes import ErrorCode
from asyncord.client.http.models import Request, Response


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
        *,
        message: str,
        request: Request,
        response: Response,
        error_body: ErrorBody | None = None,
    ) -> None:
        """Initialize the DiscordHTTPError.

        Args:
            message: Error message.
            request: Request that was sent.
            response: Response that was received.
            error_body: Body of the error.
        """
        super().__init__(message)
        self.request = request
        self.response = response
        self.error_body = error_body

    def __str__(self) -> str:
        """Format structured error to string."""
        phrase = http.HTTPStatus(self.response.status).phrase
        exc_str = f'HTTP {self.response.status} ({phrase})'

        if not self.error_body:
            if self.response.raw_body:
                return f'{exc_str}\n{self.response.raw_body}'
            return exc_str

        exc_str = f'{exc_str}\nCode {self.error_body.code}: {self.error_body.message}'
        if not self.error_body.errors:
            return exc_str

        return f'{exc_str}\n' + self._format_errors('', self.error_body.errors)

    @classmethod
    def _format_errors(cls, path: str, errors: ErrorBlock | ObjectErrorType | ArrayErrorType) -> str:
        """Get all errors from an error block.

        Args:
            path: Path to the error block.
            errors: Error block to get the errors from.

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

            error_item_str_list.append(cls._format_errors(new_path, error))

        return '\n'.join(error_item_str_list)


class ClientError(DiscordHTTPError):
    """Error raised when the client encounters an error.

    Usually this is due to a bad request (4xx).
    """

    def __init__(
        self,
        *,
        message: str,
        request: Request,
        response: Response,
        error_body: ErrorBody | None = None,
    ) -> None:
        """Initialize the ClientError.

        Args:
            message: Error message.
            request: Request that was sent.
            response: Response that was received.
            error_body: Body of the error.
        """
        super().__init__(
            message=message,
            request=request,
            response=response,
            error_body=error_body,
        )


class NotFoundError(ClientError):
    """Error raised when status code 404 occurs."""


class RateLimitError(DiscordHTTPError):
    """Error raised when the client encounters a rate limit.

    This is usually due to too many requests (429).
    """

    def __init__(
        self,
        *,
        message: str,
        request: Request,
        response: Response,
        error_body: ErrorBody | None = None,
        retry_after: float,
    ) -> None:
        """Initialize the RateLimitError.

        Args:
            message: Error message.
            request: Request that was sent.
            response: Response that was received.
            error_body: Body of the error.
            retry_after: The time in seconds until the client can make another request.
        """
        super().__init__(
            message=message,
            request=request,
            response=response,
            error_body=error_body,
        )
        self.retry_after = retry_after

    def __str__(self) -> str:
        """Format the error."""
        return f'{self.message} (retry after {self.retry_after})'


class ServerError(DiscordHTTPError):
    """Error raised when the server return status code >= 500."""

    def __init__(
        self,
        *,
        message: str,
        request: Request,
        response: Response,
        error_body: ErrorBody | None = None,
    ) -> None:
        """Initialize the ServerError.

        Args:
            message: Error message.
            request: Request that was sent.
            response: Response that was received.
            error_body: Body of the error.
        """
        super().__init__(
            message=message,
            request=request,
            response=response,
            error_body=error_body,
        )


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


class ErrorBody(BaseModel):
    """Represents a body of a response error."""

    code: ErrorCode
    """Error code."""

    message: str
    """Error message."""

    errors: ErrorBlock | ObjectErrorType | None = None
    """Error block."""
