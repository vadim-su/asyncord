"""This module contains middleware for handling HTTP errors."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, NoReturn

from asyncord.client.http import errors as htpp_errors
from asyncord.client.http.middleware.base import BaseMiddleware, NextCallType
from asyncord.client.http.models import Request, Response

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient


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
        try:
            error_body = htpp_errors.ErrorBody.model_validate(response.body)
        except ValueError as err:
            raise htpp_errors.ServerError(
                message='Failed to validate error body: {response.raw_body}',
                request=request,
                response=response,
            ) from err

        status = response.status
        if status == HTTPStatus.NOT_FOUND:
            raise htpp_errors.NotFoundError(
                message=error_body.message,
                request=request,
                response=response,
                error_body=error_body,
            )

        if HTTPStatus.BAD_REQUEST <= status < HTTPStatus.INTERNAL_SERVER_ERROR:
            raise htpp_errors.ClientError(
                message=error_body.message,
                request=request,
                response=response,
                error_body=error_body,
            )

        raise htpp_errors.ServerError(
            message=error_body.message,
            request=request,
            response=response,
            error_body=error_body,
        )
