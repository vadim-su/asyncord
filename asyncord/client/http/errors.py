from aiohttp import ClientResponse


class BaseDiscordError(Exception):
    """Base class for all Discord errors."""

    def __init__(self, message: str, resp: ClientResponse) -> None:
        self.message = message
        self.resp = resp

    def __str__(self) -> str:
        return f'{self.message}'


class ClientError(BaseDiscordError):
    """Error raised when the client encounters an error.

    Usually this is due to a bad request (4xx).
    """

    def __init__(self, message: str, resp: ClientResponse, code: int | None = None) -> None:
        super().__init__(message, resp)
        self.code = code

    def __str__(self) -> str:
        return f'({self.code}) {self.message}'


class RateLimitError(BaseDiscordError):
    """Error raised when the client encounters a rate limit.

    This is usually due to too many requests (429).
    """

    def __init__(self, message: str, resp: ClientResponse, retry_after: float | None = None) -> None:
        super().__init__(message, resp)
        self.retry_after = retry_after

    def __str__(self) -> str:
        return f'{self.message} (retry after {self.retry_after})'


class ServerError(BaseDiscordError):
    """Error raised when the server return status code >= 500."""

    def __init__(self, message: str, resp: ClientResponse, status_code: int) -> None:
        super().__init__(message, resp)
        self.status_code = status_code

    def __str__(self) -> str:
        return f'{self.status_code}: {self.message}'
