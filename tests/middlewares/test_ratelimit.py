import json
from http import HTTPStatus
from unittest.mock import AsyncMock, Mock

import pytest

from asyncord.client.http import headers
from asyncord.client.http.errors import RateLimitError
from asyncord.client.http.headers import HttpMethod
from asyncord.client.http.middleware.ratelimit import BackoffRateLimitStrategy, MaxRetriesExceededError
from asyncord.client.http.models import RatelimitResponse, Request, Response


@pytest.fixture
def rate_limit_strategy() -> BackoffRateLimitStrategy:
    """Return an instance of the BackoffRateLimitStrategy."""
    return BackoffRateLimitStrategy(max_retries=1, min_wait_time=0, max_wait_time=1)


@pytest.fixture
def ratelimit_error() -> RateLimitError:
    """Return an instance of the RateLimitError."""
    raw_body = b"""{
        "message": "Rate limit exceeded",
        "retry_after": 2,
        "global": false,
        "code": 11
    }"""

    rl_headers = {
        headers.RATELIMIT_REQUEST_LIMIT.lower(): '100',
        headers.RATELIMIT_REQUEST_REMAINING.lower(): '50',
        headers.RATELIMIT_RESET.lower(): '1629878400',
        headers.RATELIMIT_RESET_AFTER.lower(): '3600',
        headers.RATELIMIT_BUCKET.lower(): 'bucket',
    }

    return RateLimitError(
        message='Rate limit exceeded',
        request=Request(method=HttpMethod.GET, url='https://example.com'),
        response=Response(
            raw_response=Mock(),
            status=HTTPStatus.TOO_MANY_REQUESTS,
            headers=rl_headers,
            raw_body=raw_body,
            body=json.loads(raw_body),
        ),
        ratelimit_body=RatelimitResponse.model_validate_json(raw_body),
    )


async def test_handler_with_no_rate_limit_error(
    request_obj: Request,
    rate_limit_strategy: BackoffRateLimitStrategy,
) -> None:
    """Test the handler method with no rate limit error."""
    next_call = AsyncMock(
        return_value=Response(
            raw_response=Mock(),
            status=HTTPStatus.OK,
            headers={},
            raw_body=b'{"message": "OK"}',
            body={'message': 'OK'},
        ),
    )
    response = await rate_limit_strategy.handler(request_obj, Mock(), next_call)
    assert response.status == 200


async def test_handler_with_max_retries_exceeded(
    ratelimit_error: RateLimitError,
    rate_limit_strategy: BackoffRateLimitStrategy,
) -> None:
    """Test the handler method with max retries exceeded."""
    next_call = AsyncMock(
        side_effect=ratelimit_error,
    )
    with pytest.raises(MaxRetriesExceededError, match=r'Max retries exceeded') as exc_info:
        await rate_limit_strategy(ratelimit_error.request, Mock(), next_call)

    assert 1 < exc_info.value.total_wait_time < 3


async def test_handler_max_wait_time(
    ratelimit_error: RateLimitError,
    rate_limit_strategy: BackoffRateLimitStrategy,
) -> None:
    """Test the handler method with max wait time."""
    rate_limit_strategy.max_wait_time = 0
    next_call = AsyncMock(
        side_effect=ratelimit_error,
    )
    with pytest.raises(MaxRetriesExceededError, match=r'Max retries exceeded') as exc_info:
        await rate_limit_strategy(ratelimit_error.request, Mock(), next_call)

    assert exc_info.value.total_wait_time < 1
