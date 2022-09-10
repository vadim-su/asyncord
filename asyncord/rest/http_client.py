
from __future__ import annotations

import enum
import typing

import requests

import asyncord
from asyncord.rest.tokent import Token

HTTP_USER_AGENT = f'DiscordBot ({asyncord.__url__}, {asyncord.__version__})'

JSONType = dict[str, typing.Any] | list[typing.Any]


@enum.unique
class HTTPMethod(str, enum.Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class SyncHttpClient:
    def __init__(self, token: Token) -> None:
        self._session = requests.Session()
        self._session.headers.update(token.headers())
        self._session.headers.update({'User-Agent': HTTP_USER_AGENT})

    def _request(
        self, method: HTTPMethod, path: str, payload: JSONType | None = None,
    ) -> JSONType:
        with self._session as session:
            resp = session.request(str(method), path, payload)
            resp.raise_for_status()
            return resp.json()

    def get(self, path: str) -> JSONType:
        return self._request(HTTPMethod.GET, path)

    def post(self, path: str, payload: JSONType) -> JSONType:
        return self._request(HTTPMethod.POST, path, payload)

    def put(self, path: str, payload: JSONType) -> JSONType:
        return self._request(HTTPMethod.PUT, path, payload)

    def patch(self, path: str, payload: JSONType) -> JSONType:
        return self._request(HTTPMethod.PATCH, path, payload)

    def delete(self, path: str) -> JSONType:
        return self._request(HTTPMethod.DELETE, path)
