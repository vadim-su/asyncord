"""This module contains a root of the REST client for Asyncord."""

from __future__ import annotations

import aiohttp

from asyncord.client.applications.resources import ApplicationResource
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.guilds.resources import GuildResource
from asyncord.client.interactions.resources import InteractionResource
from asyncord.client.ports import AsyncHttpClientPort
from asyncord.client.resources import ClientResource
from asyncord.client.users.resources import UserResource


class RestClient(ClientResource):
    """Root of the REST client for Asyncord."""

    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession | None = None,
        http_client: AsyncHttpClientPort | None = None,
    ) -> None:
        """Initialize the REST client.

        Args:
            token: Bot token.
            session: Client session. Defaults to None.
            http_client: HTTP client. Defaults to None.
        """
        super().__init__(token, session=session, http_client=http_client)
        self.guilds = GuildResource(self)
        self.users = UserResource(self)
        self.channels = ChannelResource(self)
        self.applications = ApplicationResource(self)
        self.interactions = InteractionResource(self)
