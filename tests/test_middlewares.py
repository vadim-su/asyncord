from http import HTTPStatus
from unittest.mock import AsyncMock, Mock

import pytest

from asyncord.client.http import errors as http_errors
from asyncord.client.http.headers import HttpMethod
from asyncord.client.http.middleware.errors import ErrorHandlerMiddleware
from asyncord.client.http.models import Request, Response


@pytest.fixture()
def request_obj() -> Request:
    """Return an instance of the request model.

    request is a reserved keyword in pytest, so we use request_obj instead.
    """
    return Request(method=HttpMethod.GET, url='https://example.com')


@pytest.fixture()
def err_middleware() -> ErrorHandlerMiddleware:
    """Return an instance of the error handler middleware."""
    return ErrorHandlerMiddleware()


async def test_handler_with_no_error(request_obj: Request, err_middleware: ErrorHandlerMiddleware) -> None:
    """Test the handler method with no error."""
    next_call = AsyncMock(
        return_value=Response(
            raw_response=Mock(),
            status=HTTPStatus.OK,
            headers={},
            raw_body='{"message": "OK"}',
            body={'message': 'OK'},
        ),
    )
    response = await err_middleware.handler(request_obj, Mock(), next_call)
    assert response.status == HTTPStatus.OK


async def test_handler_with_not_found_error(request_obj: Request, err_middleware: ErrorHandlerMiddleware) -> None:
    """Test the handler method with a not found error."""
    next_call = AsyncMock(
        return_value=Response(
            raw_response=Mock(),
            status=HTTPStatus.NOT_FOUND,
            headers={},
            raw_body='{"message": "Not Found", "code": 0}',
            body={'message': 'Not Found', 'code': 0},
        ),
    )
    with pytest.raises(http_errors.NotFoundError):
        await err_middleware(request_obj, Mock(), next_call)


async def test_handler_with_client_error(request_obj: Request, err_middleware: ErrorHandlerMiddleware) -> None:
    """Test the handler method with a client error."""
    next_call = AsyncMock(
        return_value=Response(
            raw_response=Mock(),
            status=HTTPStatus.BAD_REQUEST,
            headers={},
            raw_body='{message: "Bad Request", code: 0}',
            body={'message': 'Bad Request', 'code': 0},
        ),
    )
    with pytest.raises(http_errors.ClientError):
        await err_middleware(request_obj, Mock(), next_call)


async def test_handler_with_server_error(request_obj: Request, err_middleware: ErrorHandlerMiddleware) -> None:
    """Test the handler method with a server error."""
    next_call = AsyncMock(
        return_value=Response(
            raw_response=Mock(),
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            headers={},
            raw_body='{message: "Internal Server Error", code: 0}',
            body={'message': 'Internal Server Error', 'code': 0},
        ),
    )

    with pytest.raises(http_errors.ServerError):
        await err_middleware(request_obj, Mock(), next_call)


async def test_handler_with_invalid_error_body(request_obj: Request, err_middleware: ErrorHandlerMiddleware) -> None:
    """Test the handler method with an invalid error body."""
    next_call = AsyncMock(
        return_value=Response(
            raw_response=Mock(),
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            headers={},
            raw_body='Invalid Body',
            body={},
        ),
    )
    with pytest.raises(http_errors.ServerError):
        await err_middleware(request_obj, Mock(), next_call)
