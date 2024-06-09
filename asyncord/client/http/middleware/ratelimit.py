"""This module provides middleware for authentication strategies in the Asyncord HTTP client."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from asyncord.client.http.errors import RateLimitError
from asyncord.client.http.middleware.base import BaseMiddleware, NextCallType

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.client.http.models import Request, Response

DEFAULT_BACKOFF_MAX_RETRIES: int = 3
"""Default maximum number of retries for the backoff rate limit strategy."""

DEFAULT_BACKOFF_MAX_WAIT_TIME: int = 60
"""Default maximum wait time in seconds for the backoff rate limit strategy."""


class RateLimitStrategy(BaseMiddleware):
    """Base class for rate limit strategies."""


class BackoffRateLimitStrategy(RateLimitStrategy):
    """Backoff rate limit strategy.

    This strategy will retry requests after waiting for the time specified by the rate limit headers.
    If retries exceed the maximum number of retries, the last rate limit error will be raised.

    Attributes:
        max_retries: Maximum number of retries.
        max_wait_time: Maximum wait time in seconds.
    """

    def __init__(
        self,
        max_retries: int = DEFAULT_BACKOFF_MAX_RETRIES,
        max_wait_time: int = DEFAULT_BACKOFF_MAX_WAIT_TIME,
    ):
        """Initialize strategy.

        Args:
            max_retries: Maximum number of retries. Defaults to 3.
            max_wait_time: Maximum wait time in seconds. Defaults to 60.
        """
        self.max_retries = max_retries
        self.max_wait_time = max_wait_time

    async def handler(
        self,
        request: Request,
        http_client: HttpClient,
        next_call: NextCallType,
    ) -> Response:
        """Handle global rate limits."""
        last_err = None
        for _ in range(self.max_retries + 1):
            try:
                return await next_call(request, http_client)
            except RateLimitError as err:
                last_err = err
                await asyncio.sleep(min(err.retry_after + 0.1, self.max_wait_time))

        if last_err:
            raise last_err

        raise RuntimeError(f'RateLimitError was not raised after max retries ({self.max_retries})')
