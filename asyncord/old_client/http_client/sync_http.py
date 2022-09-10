import enum
import typing

import requests

import asyncord

HTTP_USER_AGENT = f'DiscordBot ({asyncord.__url__}, {asyncord.__version__})'

JSONType = dict[str, typing.Any] | list[typing.Any]


@enum.unique
class Method(str, enum.Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class SyncHttpClient:
    def __init__(self, token: str):
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': HTTP_USER_AGENT,
            'Authorization': f'Bot {token}',
        })

    def _request(self, method, url, payload=None) -> JSONType:
        resp = self._session.request(method, url, payload)
        resp.raise_for_status()
        return resp.json()

    def get(self, url) -> JSONType:
        return self._request(Method.GET, url)

    def post(self, url, payload=None) -> JSONType:
        return self._request(Method.POST, url, payload)

    def put(self, url, payload=None) -> JSONType:
        return self._request(Method.PUT, url, payload)

    def patch(self, url, payload=None) -> JSONType:
        return self._request(Method.PATCH, url, payload)

    def delete(self, url, payload=None) -> JSONType:
        return self._request(Method.DELETE, url, payload)
