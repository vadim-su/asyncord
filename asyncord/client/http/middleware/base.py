"""This module contains the Proxy class.

This class controls the incoming calls to http_client.
And handles the limits with strategy.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Protocol

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.client.http.models import Request, Response

__all__ = ('BaseMiddleware', 'Middleware', 'NextCallType', 'RateLimitBody')

logger = logging.getLogger(__name__)

type NextCallType = Callable[[Request, HttpClient], Awaitable[Response]]


class RateLimitBody(BaseModel):
    """The body of a rate limit response."""

    message: str
    """Message saying you are being rate limited."""

    retry_after: float
    """Number of seconds to wait before submitting another request."""

    is_global: bool = Field(alias='global')
    """Whether this is a global rate limit."""


class Middleware(Protocol):
    """Middleware protocol."""

    async def __call__(
        self,
        request: Request,
        http_client: HttpClient,
        next_call: NextCallType,
    ) -> Response:
        """Middleware call."""
        ...


class BaseMiddleware(ABC):  # pragma: no cover
    """Base middleware class."""

    @abstractmethod
    async def handler(
        self,
        request: Request,
        http_client: HttpClient,
        next_call: NextCallType,
    ) -> Response:
        """Middleware handler.

        I separated this method from __call__ to make it less confusing than __call__
        on defining the middleware.
        """
        raise NotImplementedError

    async def __call__(
        self,
        request: Request,
        http_client: HttpClient,
        next_call: NextCallType,
    ) -> Response:
        """Middleware call."""
        return await self.handler(request, http_client, next_call)
