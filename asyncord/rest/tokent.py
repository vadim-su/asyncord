"""Entities of tokens permitted in Discord API."""

from abc import ABC, abstractmethod


class Token(ABC):
    """A base abstract class for all token types."""

    def __init__(self, token_value: str) -> None:
        self._token_value = token_value

    @abstractmethod
    def headers(self) -> dict[str, str]:
        """Generate a list of authorization headers."""


class BotToken(Token):
    """Represents a bot token that can be used to interact with discord API as a bot."""

    def headers(self) -> dict[str, str]:
        return {'Authorization': f'Bot {self._token_value}'}


class BearerToken(Token):
    """Represents a bearer token that can be used to interact with discord API."""

    def headers(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self._token_value}'}
