import typing

from asyncord.client.base import BaseRestClient

from .base import HttpClient, BaseRestClient
from .guilds import _GuildRestClient

JSONType = dict[str, typing.Any] | list[typing.Any]


class RootRestClient(BaseRestClient):
    def __init__(self, token: str, http_client: HttpClient):
        super().__init__(token, http_client)
        self.guilds = _GuildRestClient(self)
