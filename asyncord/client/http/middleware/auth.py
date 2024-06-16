"""Module for authentication strategy middleware."""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.http.middleware.base import BaseMiddleware

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.client.http.middleware.base import NextCallType
    from asyncord.client.http.models import Request, Response

__all__ = ('AuthStrategy', 'BotTokenAuthStrategy')


class AuthStrategy(BaseMiddleware):
    """Base class for authentication strategies."""


class BotTokenAuthStrategy(AuthStrategy):
    """Bot token authentication strategy."""

    def __init__(self, token: str):
        """Initialize the middleware."""
        self.token = token

    async def handler(
        self,
        request: Request,
        http_client: HttpClient,
        next_call: NextCallType,
    ) -> Response:
        """Add bot token to the Authorization header."""
        request.headers['Authorization'] = f'Bot {self.token}'
        return await next_call(request, http_client)
