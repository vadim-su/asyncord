import typing


class CredentionalStrategy(typing.Protocol):
    async def acquire(self) -> str:
        ...


class BotToken():
    def __init__(self, token: str) -> None:
        self._token = token

    async def acqire(self) -> str:
        return self._token
