import typing

JSONType = dict[str, typing.Any] | list[typing.Any]


class HttpClient(typing.Protocol):
    def set_headers(self, headers: dict[str, str]):
        ...

    async def get(self, url: str) -> JSONType:
        ...

    async def put(self, url: str, payload: JSONType) -> JSONType:
        ...

    async def post(self, url: str, payload: JSONType) -> JSONType:
        ...

    async def patch(self, url: str, payload: JSONType) -> JSONType:
        ...

    async def delete(self, url: str, payload: JSONType = None) -> JSONType:
        ...
