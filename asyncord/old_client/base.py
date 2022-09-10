import typing

import asyncord

HTTP_USER_AGENT = f'DiscordBot ({asyncord.__url__}, {asyncord.__version__})'

JSONType = dict[str, typing.Any] | list[typing.Any]


class BaseRestClient:
    def __init__(self, token: str, http_client: HttpClient):
        self.token = token
        self._http = http_client
