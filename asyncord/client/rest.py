from __future__ import annotations

from asyncord.snowflake import Snowflake
from asyncord.client.users import UserResource
from asyncord.client.guilds import GuildResource
from asyncord.client.channels import ChannelResource
from asyncord.client.resources import ClientResource
from asyncord.client.http_proto import AsyncHttpClientPort


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


TOKEN = 'OTM0NTY0MjI1NzY5MTQ4NDM2.Yex6wg.AAkUaqRS0ACw8__ERfQ6d8gOdkE'

KOSTOMEISTER_HABITATION = Snowflake(763522265874694144)


async def main():
    from pprint import pprint
    async with RestClient(TOKEN) as client:
        resp = await client.guilds.get_preview(KOSTOMEISTER_HABITATION)
        pprint(resp.body)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
