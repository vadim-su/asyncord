from __future__ import annotations

from asyncord.client.ports import AsyncHttpClientPort
from asyncord.client.users import UserResource
from asyncord.client.guilds import GuildResource
from asyncord.client.channels import ChannelResource
from asyncord.client.resources import ClientResource


class RestClient(ClientResource):
    def __init__(self, token: str, *, http_client: AsyncHttpClientPort | None = None) -> None:
        super().__init__(token, http_client=http_client)
        self.guilds = GuildResource(self)
        self.users = UserResource(self)
        self.channels = ChannelResource(self)

    @classmethod
    async def create(cls, token: str, *, http_client: AsyncHttpClientPort | None = None) -> RestClient:
        client = cls(token, http_client=http_client)
        client.start()
        return client

    def start(self):
        self._http.start()

    async def close(self):
        await self._http.close()

    async def __aenter__(self) -> RestClient:
        self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
