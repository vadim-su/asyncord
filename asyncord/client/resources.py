"""This module contains the base classes for client resources."""

from __future__ import annotations

import aiohttp

from asyncord.client.http.bucket_track import BucketTrack
from asyncord.client.http.client import AsyncHttpClient
from asyncord.client.http.headers import AUTHORIZATION
from asyncord.client.http.middleware import BasicMiddleWare, MiddleWare


class ClientResource:
    """Base class for client resources."""

    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession | None = None,
        http_client: AsyncHttpClient | None = None,
        middleware: MiddleWare | None = None,
    ) -> None:
        """Initialize the resource.

        Args:
            token: Bot token.
            session: Client session. Defaults to None.
            http_client: HTTP client. Defaults to None.
            middleware: Middleware. Defaults to basic one.
        """
        self._token = token
        if http_client:
            self._http_client = http_client
        else:
            self._http_client: AsyncHttpClient = AsyncHttpClient(
                session=session,
            )

        if middleware:
            self._http_client.middleware = middleware
        else:
            self._http_client.middleware = BasicMiddleWare(
                headers={AUTHORIZATION: f'Bot {token}'},
                bucket_tracker=BucketTrack(),
            )


class ClientSubresource(ClientResource):
    """Base class for client subresources."""

    def __init__(self, parent: ClientResource) -> None:
        """Initialize the subresource.

        Args:
            parent: Parent resource.
        """
        super().__init__(parent._token, http_client=parent._http_client)
