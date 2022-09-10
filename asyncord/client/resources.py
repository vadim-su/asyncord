from __future__ import annotations

from asyncord.client.headers import AUTHORIZATION
from asyncord.client.http_proto import AsyncHttpClientPort
from asyncord.client.http_client import AsyncHttpClient


class ClientResource:
    def __init__(self, token: str, *, http_client: AsyncHttpClientPort | None = None) -> None:
        self.token = token

        if http_client is None:
            http_client = AsyncHttpClient()

        self._http = http_client
        self._http.set_headers({AUTHORIZATION: f'Bot {token}'})


class ClientSubresources(ClientResource):
    def __init__(self, parent: ClientResource) -> None:
        super().__init__(parent.token, http_client=parent._http)
