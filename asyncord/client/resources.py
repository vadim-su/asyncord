from __future__ import annotations

from asyncord.client.headers import AUTHORIZATION
from asyncord.client.http_proto import AsyncHttpClientPort
from asyncord.client.http_client import AsyncHttpClient


class ClientResource:
    """Base class for client resources."""

    def __init__(self, token: str, *, http_client: AsyncHttpClientPort | None = None) -> None:
        """Initialize the resource.

        Args:
            token (str): Bot token.
            http_client (AsyncHttpClientPort | None): HTTP client. Defaults to None.
        """
        self.token = token

        if http_client:
            self._http = http_client
        else:
            self._http: AsyncHttpClientPort = AsyncHttpClient()

        self._http.set_headers({AUTHORIZATION: f'Bot {token}'})


# FIXME: Candidate for removal
class ClientSubresources(ClientResource):
    """Base class for client subresources.

    Subresources are resources that are accessed through another resource.
    For example, the messages resource is accessed through the channels resource.
    """

    def __init__(self, parent: ClientResource) -> None:
        """Initialize the subresource.

        Args:
            parent (ClientResource): The parent resource.
        """
        super().__init__(parent.token, http_client=parent._http)  # noqa: WPS437 - Found protected attribute
