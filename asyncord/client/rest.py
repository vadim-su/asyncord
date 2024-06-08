"""This module contains a root of the REST client for Asyncord."""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.applications.resources import ApplicationResource
from asyncord.client.auth.resources import OAuthResource
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.guilds.resources import GuildResource
from asyncord.client.http.client import HttpClient
from asyncord.client.http.middleware.auth import BotTokenAuthStrategy
from asyncord.client.interactions.resources import InteractionResource
from asyncord.client.invites.resources import InvitesResource
from asyncord.client.stage_instances.resources import StageInstancesResource
from asyncord.client.users.resources import UserResource
from asyncord.client.webhooks.resources import WebhooksResource

if TYPE_CHECKING:
    import aiohttp

    from asyncord.client.http.middleware.auth import AuthStrategy


class RestClient:
    """Root of the REST client for Asyncord."""

    def __init__(
        self,
        auth: str | AuthStrategy | None,
        session: aiohttp.ClientSession | None = None,
        http_client: HttpClient | None = None,
    ) -> None:
        """Initialize the resource.

        Args:
            auth: Auth strategy to use for authentication.
                If str is passed, it is treated as a bot token.
                If None is passed, you need to pass a custom http_client.
            session: Client session. Defaults to None.
            http_client: HTTP client. Defaults to None.
            middleware: Middleware. Defaults to basic one.
        """
        if http_client:
            if session:
                err = ValueError('Cannot pass both session and http_client.')
                err.add_note(
                    'If you pass http_client you should set its session attribute.',
                )
                raise err
            self._http_client = http_client
        else:
            if not auth:
                err = ValueError('Auth strategy is required if you do not pass custom http_client.')
                err.add_note(
                    'None value is allowed only if you pass custom http_client, because it can do its own auth.',
                )
                err.add_note(
                    'If you want to use default http_client, you need to pass a valid auth strategy.',
                )
                raise err
            self._http_client: HttpClient = HttpClient(session=session)

        if not auth:
            return

        if isinstance(auth, str):
            auth = BotTokenAuthStrategy(auth)

        self._http_client.system_middlewares.append(auth)

        # Initialize resources
        self.guilds = GuildResource(self._http_client)
        self.users = UserResource(self._http_client)
        self.channels = ChannelResource(self._http_client)
        self.applications = ApplicationResource(self._http_client)
        self.interactions = InteractionResource(self._http_client)
        self.invites = InvitesResource(self._http_client)
        self.stage_instances = StageInstancesResource(self._http_client)
        self.webhooks = WebhooksResource(self._http_client)
        self.auth = OAuthResource(self._http_client)
