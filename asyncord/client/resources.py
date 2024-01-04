"""This module contains the base classes for client resources."""

from __future__ import annotations

from asyncord.client.http.client import AsyncHttpClient
from asyncord.client.http.headers import AUTHORIZATION
from asyncord.client.ports import AsyncHttpClientPort


class ClientResource:
    """Base class for client resources."""

    def __init__(self, token: str, *, http_client: AsyncHttpClientPort | None = None) -> None:
        self._token = token
        if http_client:
            self._http_client = http_client
        else:
            self._http_client: AsyncHttpClientPort = AsyncHttpClient(
                headers={AUTHORIZATION: f"Bot {token}"},
            )


class ClientSubresource(ClientResource):
    """Base class for client subresources."""

    def __init__(self, parent: ClientResource) -> None:
        super().__init__(
            parent._token, http_client=parent._http_client,
        )
