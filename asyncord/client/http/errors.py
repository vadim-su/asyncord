"""This module contains all the errors that can be raised by the HTTP client."""

from __future__ import annotations

import http
from typing import TYPE_CHECKING

from asyncord.client.http.models import (
    ErrorBlock,
    RateLimitHeaders,
)

if TYPE_CHECKING:
    from asyncord.client.http.models import (
        ArrayErrorType,
        ErrorResponse,
        ObjectErrorType,
        RatelimitResponse,
        Request,
        Response,
    )

__all__ = (
    'BaseDiscordError',
    'ClientError',
    'DiscordHTTPError',
    'NotFoundError',
    'RateLimitError',
    'ServerError',
)


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
        error_body: ErrorResponse | None = None,
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
        self.ratelimit_headers = RateLimitHeaders.model_validate(response.headers)

    def __str__(self) -> str:
        """Format structured error to string."""
        phrase = http.HTTPStatus(self.response.status).phrase
        exc_str = [f'HTTP {self.response.status} ({phrase})']

        if self.error_body:
            exc_str.append(f'Code {self.error_body.code}: {self.error_body.message}')
            if self.error_body.errors:
                exc_str.append(self._format_errors('', self.error_body.errors))

        elif self.response.raw_body:
            exc_str.append(self.response.raw_body.decode(errors='backslashreplace'))

        return '\n'.join(exc_str)

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

        # fmt: off
        error_items = (
            cls._format_errors(f'{path}.{field_name}', error)
            if path else str(field_name)
            for field_name, error in errors.items()
        )
        # fmt: on

        return '\n'.join(error_items)


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
        error_body: ErrorResponse | None = None,
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
        ratelimit_body: RatelimitResponse,
    ) -> None:
        """Initialize the RateLimitError.

        Args:
            message: Error message.
            request: Request that was sent.
            response: Response that was received.
            ratelimit_body: Rate limit response.
        """
        super().__init__(
            message=message,
            request=request,
            response=response,
            error_body=None,
        )
        self.rate_limit_body = ratelimit_body
        self.retry_after = ratelimit_body.retry_after

    def __str__(self) -> str:
        """Format the error."""
        resp = self.rate_limit_body
        return f'{resp.message} (retry after: {resp.retry_after}s, global: {resp.is_global}, code: {resp.code})'


class ServerError(DiscordHTTPError):
    """Error raised when the server return status code >= 500."""

    def __init__(
        self,
        *,
        message: str,
        request: Request,
        response: Response,
        error_body: ErrorResponse | None = None,
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
