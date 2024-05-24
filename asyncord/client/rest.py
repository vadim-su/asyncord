"""This module contains a root of the REST client for Asyncord."""

from __future__ import annotations

import aiohttp

from asyncord.client.applications.resources import ApplicationResource
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.guilds.resources import GuildResource
from asyncord.client.http.client import AsyncHttpClient
from asyncord.client.interactions.resources import InteractionResource
from asyncord.client.invites.resources import InvitesResource
from asyncord.client.resources import ClientResource
from asyncord.client.stage_instances.resources import StageInstancesResource
from asyncord.client.stickers.resources import StickersResource
from asyncord.client.users.resources import UserResource


class RestClient(ClientResource):
    """Root of the REST client for Asyncord."""

    def __init__(
        self,
        token: str,
        session: aiohttp.ClientSession | None = None,
        http_client: AsyncHttpClient | None = None,
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
        self.invites = InvitesResource(self)
        self.stage_instances = StageInstancesResource(self)
        self.stickers = StickersResource(self)
