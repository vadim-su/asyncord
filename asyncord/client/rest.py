"""This module contains a root of the REST client for Asyncord."""

from __future__ import annotations

from asyncord.client.applications.resources import ApplicationResource
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.guilds.resources import GuildResource
from asyncord.client.interactions.resources import InteractionResource
from asyncord.client.ports import AsyncHttpClientPort
from asyncord.client.resources import ClientResource
from asyncord.client.users.resources import UserResource


class RestClient(ClientResource):
    def __init__(self, token: str, *, http_client: AsyncHttpClientPort | None = None) -> None:
        super().__init__(token, http_client=http_client)
        self.guilds = GuildResource(self)
        self.users = UserResource(self)
        self.channels = ChannelResource(self)
        self.applications = ApplicationResource(self)
        self.interactions = InteractionResource(self)

    @classmethod
    async def create(cls, token: str, *, http_client: AsyncHttpClientPort | None = None) -> RestClient:
        client = cls(token, http_client=http_client)
        client.start()
        return client

    def start(self):
        self._http_client.start()

    async def close(self):
        await self._http_client.close()

    async def __aenter__(self) -> RestClient:
        self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
