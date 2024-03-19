"""This module contains the base classes for client resources."""

from __future__ import annotations

import aiohttp

from asyncord.client.http.client import AsyncHttpClient
from asyncord.client.http.headers import AUTHORIZATION
from asyncord.client.ports import AsyncHttpClientPort


class ClientResource:
    """Base class for client resources."""

    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession | None = None,
        http_client: AsyncHttpClientPort | None = None,
    ) -> None:
        """Initialize the resource.

        Args:
            token: Bot token.
            session: Client session. Defaults to None.
            http_client: HTTP client. Defaults to None.
        """
        self._token = token
        if http_client:
            self._http_client = http_client
        else:
            self._http_client: AsyncHttpClientPort = AsyncHttpClient(
                session=session,
                headers={AUTHORIZATION: f'Bot {token}'},
            )


class ClientSubresource(ClientResource):
    """Base class for client subresources."""

    def __init__(self, parent: ClientResource) -> None:
        """Initialize the subresource.

        Args:
            parent: Parent resource.
        """
        super().__init__(parent._token, http_client=parent._http_client)
