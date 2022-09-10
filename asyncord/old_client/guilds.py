from __future__ import annotations

import typing

from asyncord import urls

from . import base

if typing.TYPE_CHECKING:
    from .client import RootRestClient


class _GuildRestClient(base.BaseRestClient):
    guilds_url = f'{urls.REST_API_URL}/guilds'
    guild_url = f'{guilds_url}/guild'

    def __init__(self, root: RootRestClient):
        super().__init__(root.token, root._http)

    async def create_guild(self, **kwargs):
        return await self._http.post(self.guilds_url, kwargs)

    async def get_guild(self, guild_id: str) -> base.JSONType:
        url = f'{self.guilds_url}/{guild_id}'
        return await self._http.get(url)

    async def get_preview(self, guild_id: str) -> base.JSONType:
        url = f'{self.guilds_url}/{guild_id}/preview'
        return await self._http.get(url)

    async def update_guild(self, guild_id: str, **kwargs) -> base.JSONType:
        url = f'{self.guilds_url}/{guild_id}'
        return await self._http.patch(url, kwargs)

    async def delete_guild(self, guild_id: str) -> None:
        url = f'{self.guilds_url}/{guild_id}'
        await self._http.delete(url)
