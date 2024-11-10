"""This module contains the client hub to process multiple clients."""

# TODO: Add example usage of the client hub.
from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self

import aiohttp

from asyncord.client.http.middleware.auth import AuthStrategy, BotTokenAuthStrategy
from asyncord.client.rest import RestClient
from asyncord.gateway.client.client import GatewayClient
from asyncord.gateway.client.heartbeat import HeartbeatFactory
from asyncord.gateway.dispatcher import EventDispatcher
from asyncord.typedefs import Unset, UnsetType

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.client.http.middleware.ratelimit import RateLimitStrategy

__all__ = ('ClientGroup', 'ClientHub')

logger = logging.getLogger(__name__)


class ClientHub:
    """Hub to process multiple clients.

    This class is responsible for managing multiple clients.
    It can use a provided aiohttp.ClientSession or create a new one if none is provided.
    It also allows for custom HeartbeatFactory and EventDispatcher types.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        heartbeat_factory_type: type[HeartbeatFactory] = HeartbeatFactory,
    ) -> None:
        """Initialize hub to process multiple clients.

        Args:
            session: Optional session to use for the clients.
                If none is provided, a new one is created.
            heartbeat_factory_type: Factory to create heartbeat clients.
                Defaults to HeartbeatFactory.
            event_dispatcher_type: Event dispatcher to use for the clients.
                Defaults to EventDispatcher.
        """
        if session:
            self.session = session
            self._is_outer_session = True
        else:
            self.session = aiohttp.ClientSession()
            self._is_outer_session = False

        self.heartbeat_factory = heartbeat_factory_type()
        self.client_groups: dict[str, ClientGroup] = {}  # Added type annotation

        logger.info('New ClientHub instance created.')  # Added logging

    @classmethod
    @asynccontextmanager
    async def connect(
        cls,
        auth: str | AuthStrategy | None = None,
        ratelimit_strategy: RateLimitStrategy | None | UnsetType = Unset,
        session: aiohttp.ClientSession | None = None,
        dispatcher: EventDispatcher | None = None,
        http_client: HttpClient | None = None,
    ) -> AsyncGenerator[ClientGroup, None]:
        """Create a set of clients only for a single token.

        Use this method if you want to run only one application with a single token.
        In general, it is what you need.

        Args:
            auth: Auth strategy to use for authentication.
                If str is passed, it is treated as a bot token.
                If None is passed, you need to pass a custom http_client.
            ratelimit_strategy: Rate limit strategy to use.
                if didn't pass, default backoff strategy is used.
                if passed None, no rate limit strategy is used.
            session: Client session.
            dispatcher: Event dispatcher to use for the clients.
            http_client: HTTP client.

        Returns:
            A set of clients to interact with Discord.
        """
        async with cls(session=session) as hub:
            yield hub.create_client_group(
                group_name='default',
                auth=auth,
                ratelimit_strategy=ratelimit_strategy,
                dispatcher=dispatcher,
                http_client=http_client,
            )

    def create_client_group(
        self,
        group_name: str,
        auth: str | AuthStrategy | None = None,
        ratelimit_strategy: RateLimitStrategy | None | UnsetType = Unset,
        dispatcher: EventDispatcher | None = None,
        http_client: HttpClient | None = None,
    ) -> ClientGroup:
        """Create a set of clients to interact with Discord.

        Args:
            Build a set of clients to interact with Discord.

        Args:
            group_name: Name of the set.
            auth: Auth strategy to use for authentication.
                If str is passed, it is treated as a bot token.
                If None is passed, you need to pass a custom http_client.
            ratelimit_strategy: Rate limit strategy to use.
                if didn't pass, default backoff strategy is used.
                if passed None, no rate limit strategy is used.
            dispatcher: Event dispatcher to use for the clients.
            http_client: HTTP client.

        Returns:
            A set of clients to interact with Discord.
        """
        if group_name in self.client_groups:
            raise ValueError(f'Client group {group_name} already exists')

        client_group = self._build_client_group(
            group_name=group_name,
            auth=auth,
            ratelimit_strategy=ratelimit_strategy,
            session=self.session,
            dispatcher=dispatcher,
            http_client=http_client,
        )
        if not dispatcher:
            dispatcher = client_group.dispatcher
            dispatcher.add_argument('client', client_group.rest_client)
            dispatcher.add_argument('gateway', client_group.gateway_client)
            dispatcher.add_argument('client_groups', self.client_groups)
        else:
            logger.warning('Event dispatcher is passed. Make sure to add the required arguments.')

        self.client_groups[group_name] = client_group
        return client_group

    async def start(self) -> None:
        """Run client hub to process multiple clients.

        When the hub is running, it will connect to the Discord clients and process the events.
        """
        logger.info(':satellite: Connecting to Discord', extra={'markup': True})
        self.heartbeat_factory.start()
        tasks = [client.connect() for client in self.client_groups.values()]
        try:
            await asyncio.gather(*tasks)
        except (KeyboardInterrupt, asyncio.CancelledError):
            logger.info('Shutting down...')
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Stop the client hub."""
        for client in self.client_groups.values():
            await client.close()
        self.heartbeat_factory.stop()
        if not self._is_outer_session:
            await self.session.close()
        logger.info(':wave: Shutdown complete', extra={'markup': True})

    def __del__(self) -> None:
        """Log unclosed session for debugging."""
        if not self.session.closed:
            logger.warning('Unclosed client session detected', extra={'markup': True})

    async def __aenter__(self) -> Self:
        """Enter the context manager."""
        return self

    async def __aexit__(self, _exc_type, _exc, _tb) -> None:  # noqa: ANN001
        """Exit the context manager."""
        await self.start()

    def _build_client_group(
        self,
        group_name: str,
        auth: str | AuthStrategy | None,
        ratelimit_strategy: RateLimitStrategy | None | UnsetType,
        session: aiohttp.ClientSession | None,
        dispatcher: EventDispatcher | None,
        http_client: HttpClient | None,
    ) -> ClientGroup:
        """Build a set of clients to interact with Discord.

        Args:
            group_name: Name of the set.
            auth: Auth strategy to use for authentication.
                If str is passed, it is treated as a bot token.
                If None is passed, you need to pass a custom http_client.
            ratelimit_strategy: Rate limit strategy to use.
                if didn't pass, default backoff strategy is used.
                if passed None, no rate limit strategy is used.
            session: Client session.
            dispatcher: Event dispatcher to use for the clients.
            http_client: HTTP client.

        Returns:
            A set of clients to interact with Discord.
        """
        if dispatcher is None:
            dispatcher = EventDispatcher()

        rest_client = RestClient(
            auth=auth,
            ratelimit_strategy=ratelimit_strategy,
            session=session,
            http_client=http_client,
        )
        if isinstance(auth, str | BotTokenAuthStrategy):
            gateway_client = GatewayClient(
                token=auth,
                session=self.session,
                heartbeat_class=self.heartbeat_factory,
                dispatcher=dispatcher,
                name=group_name,
            )
        else:
            gateway_client = None
            logger.warning('Gateway client requires a token to connect. It will not be created.')

        return ClientGroup(
            name=group_name,
            dispatcher=dispatcher,
            rest_client=rest_client,
            gateway_client=gateway_client,
        )


@dataclass
class ClientGroup:
    """Group of clients.

    Include clients to interact with Discord.
    """

    name: str
    """Name of the set."""

    dispatcher: EventDispatcher
    """Event dispatcher."""

    rest_client: RestClient
    """Discord REST client."""

    gateway_client: GatewayClient | None  # type: ignore
    """Discord gateway client."""

    _gateway_client: GatewayClient | None = field(init=False, repr=False, default=None)
    """Masked gateway client."""

    @property
    def gateway_client(self) -> GatewayClient:
        """Discord gateway client."""
        if not self._gateway_client:
            raise ValueError('Gateway client is not created. Did you pass a token?')
        return self._gateway_client

    @gateway_client.setter
    def gateway_client(self, gateway_client: GatewayClient | None) -> None:
        """Set the gateway client."""
        self._gateway_client = gateway_client

    async def connect(self) -> None:
        """Connect to the Discord client.

        It will block until the connection is closed.

        Currently, it only connects to the gateway client, because the other clients are
        stateless and don't need to be connected.
        """
        await self.gateway_client.connect()

    async def close(self) -> None:
        """Close the connection to the Discord client."""
        await self.gateway_client.close()
