"""This module contains middleware for handling HTTP errors."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, NoReturn, cast

from asyncord.client.http import errors as http_errors
from asyncord.client.http.middleware.base import BaseMiddleware
from asyncord.client.http.models import ErrorResponse, RatelimitResponse

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.client.http.middleware.base import NextCallType
    from asyncord.client.http.models import Request, Response

__all__ = ('ErrorHandlerMiddleware',)


class ErrorHandlerMiddleware(BaseMiddleware):
    """Middleware that handles HTTP errors and raises exceptions."""

    async def handler(self, request: Request, http_client: HttpClient, next_call: NextCallType) -> Response:
        """Handle the request and raise exceptions for HTTP errors."""
        response = await next_call(request, http_client)
        if response.status < HTTPStatus.BAD_REQUEST:
            return response

        return self._raise_for_status(request, response)

    @classmethod
    def _raise_for_status(cls, request: Request, response: Response) -> NoReturn:
        """Raise an exception for the given response.

        Args:
            request: Request that was sent.
            response: Response to raise an exception for.

        Raises:
            NotFoundError: If the response status is 404.
            ClientError: If the response status is 4xx.
            ServerError: If the response status is 5xx.
        """
        if response.status is HTTPStatus.TOO_MANY_REQUESTS:
            error_body_model = RatelimitResponse
        else:
            error_body_model = ErrorResponse

        try:
            error_body = error_body_model.model_validate(response.body)
        except ValueError as err:
            raise http_errors.ServerError(
                message='Failed to validate error body: {response.raw_body}',
                request=request,
                response=response,
            ) from err

        match response.status:
            case HTTPStatus.NOT_FOUND:
                raise http_errors.NotFoundError(
                    message=error_body.message,
                    request=request,
                    response=response,
                    error_body=cast(ErrorResponse, error_body),
                )

            case HTTPStatus.TOO_MANY_REQUESTS:
                raise http_errors.RateLimitError(
                    message=error_body.message,
                    request=request,
                    response=response,
                    ratelimit_body=cast(RatelimitResponse, error_body),
                )

            case status if HTTPStatus.BAD_REQUEST <= status < HTTPStatus.INTERNAL_SERVER_ERROR:
                raise http_errors.ClientError(
                    message=error_body.message,
                    request=request,
                    response=response,
                    error_body=cast(ErrorResponse, error_body),
                )

        raise http_errors.ServerError(
            message=error_body.message,
            request=request,
            response=response,
            error_body=cast(ErrorResponse, error_body),
        )
