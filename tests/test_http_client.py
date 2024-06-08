import json
from http import HTTPStatus
from unittest.mock import ANY, AsyncMock, Mock

import aiohttp
import pytest
from pytest_mock import MockFixture

from asyncord.client.http.client import HttpClient
from asyncord.client.http.middleware.base import Middleware, NextCallType
from asyncord.client.http.models import Request, Response


@pytest.mark.parametrize('session', [Mock(), None])
@pytest.mark.parametrize(
    ('method', 'url', 'headers', 'payload'),
    [
        pytest.param(
            'GET',
            'https://example.com',
            {'Authorization': 'Bearer token'},
            None,
            id='GET request',
        ),
        pytest.param(
            'POST',
            'https://example.com',
            {'Authorization': 'Bearer token'},
            {'key': 'value'},
            id='POST request',
        ),
        pytest.param(
            'PUT',
            'https://example.com',
            {'Authorization': 'Bearer token'},
            {'key': 'value'},
            id='PUT request',
        ),
        pytest.param(
            'PATCH',
            'https://example.com',
            {'Authorization': 'Bearer token'},
            {'key': 'value'},
            id='PATCH request',
        ),
        pytest.param(
            'DELETE',
            'https://example.com',
            {'Authorization': 'Bearer token'},
            None,
            id='DELETE request',
        ),
    ],
)
async def test_http_client_general_methods(
    session: aiohttp.ClientSession | None,
    method: str,
    url: str,
    headers: dict[str, str],
    payload: dict[str, str] | None,
    mocker: MockFixture,
) -> None:
    """Complete test for the HTTP client general methods.

    This test looks complex, but it's actually quite simple. It's not super necessary
    to test every single method of the HTTP client, but it's good to have a test that
    covers all of them.
    """
    if session:
        request_mock = mocker.patch.object(session, 'request')
    else:
        request_mock = mocker.patch('aiohttp.request')

    client = HttpClient(session)
    client_method = getattr(client, method.lower())
    if payload is not None:
        await client_method(url=url, headers=headers, payload=payload)
    else:
        await client_method(url=url, headers=headers)

    request_mock.assert_called_once_with(
        method=method,
        url=url,
        headers=headers,
        data=ANY,  # Check data later.
    )

    # Some methods don't have payloads, so we need to check if the payload is correct.
    if payload is not None:
        data_arg = request_mock.call_args.kwargs['data']
        assert json.loads(data_arg._value) == payload


async def test_extract_body_no_content() -> None:
    """Test extracting body from a response with no content."""
    resp = Mock(status=HTTPStatus.NO_CONTENT)
    result = await HttpClient._extract_body(resp)
    assert result == {}


async def test_extract_body_valid_json() -> None:
    """Test extracting body from a response with valid JSON."""
    resp = Mock(status=HTTPStatus.OK, headers={'Content-Type': 'application/json'})
    resp.json = AsyncMock(return_value={'key': 'value'})
    result = await HttpClient._extract_body(resp)
    assert result == {'key': 'value'}


async def test_extract_body_invalid_json() -> None:
    """Test extracting body from a response with invalid JSON."""
    resp = Mock(status=HTTPStatus.OK, headers={'Content-Type': 'application/json'})
    resp.json = AsyncMock(side_effect=json.JSONDecodeError('Invalid JSON', '', 0))
    resp.text = AsyncMock(return_value='Invalid JSON')
    result = await HttpClient._extract_body(resp)
    assert result == {}


async def test_extract_body_not_json() -> None:
    """Test extracting body from a response that is not JSON."""
    resp = Mock(status=HTTPStatus.OK, headers={'Content-Type': 'text/plain'})
    result = await HttpClient._extract_body(resp)
    assert result == {}


async def test_apply_middleware(mocker: MockFixture) -> None:
    """Test applying middleware to a request.

    We need to be sure that the middleware is called in the correct order.
    """
    middleware_index = 0
    raw_request_mock = mocker.patch(
        'asyncord.client.http.client.HttpClient._raw_request',
        return_value={},
        kwargs={'call_order': 0},
    )
    system_middleware = Mock(kwargs={'call_order': 0})
    middleware1 = Mock(kwargs={'call_order': 0})
    middleware2 = Mock(kwargs={'call_order': 0})

    def _middleware_wrap(mock: AsyncMock) -> Middleware:
        async def wrapper(request: Request, http_client: HttpClient, next_call: NextCallType) -> Response:
            nonlocal middleware_index
            middleware_index += 1
            mock.call_order = middleware_index
            return await next_call(request, http_client)

        return wrapper

    client = HttpClient(
        middlewares=[
            _middleware_wrap(middleware1),
            _middleware_wrap(middleware2),
        ],
    )
    client.system_middlewares.append(_middleware_wrap(system_middleware))

    request_mock = Mock()
    await client._apply_middleware(request_mock)

    raw_request_mock.assert_called_once_with(request_mock)
    assert middleware1.call_order < middleware2.call_order < system_middleware.call_order
