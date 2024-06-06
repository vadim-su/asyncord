"""This module contains the client hub to process multiple clients."""

# TODO: Add example usage of the client hub.
from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import NamedTuple, Self

import aiohttp

from asyncord.client.http.bucket_track import BucketTrack
from asyncord.client.http.client import AsyncHttpClient
from asyncord.client.http.middleware import BasicMiddleWare
from asyncord.client.rest import RestClient
from asyncord.gateway.client.client import GatewayClient
from asyncord.gateway.client.heartbeat import HeartbeatFactory
from asyncord.gateway.dispatcher import EventDispatcher

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
        event_dispatcher_type: type[EventDispatcher] = EventDispatcher,
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
            self._outer_session = True
        else:
            self.session = aiohttp.ClientSession()
            self._outer_session = False

        self.heartbeat_factory = heartbeat_factory_type()
        self.client_groups: dict[str, ClientGroup] = {}  # Added type annotation

        self.event_dispatcher_type = event_dispatcher_type

        logger.info('New ClientHub instance created.')  # Added logging

    @classmethod
    @asynccontextmanager
    async def setup_single_client_group(
        cls,
        token: str,
        session: aiohttp.ClientSession | None = None,
        heartbeat_factory_type: type[HeartbeatFactory] = HeartbeatFactory,
        dispatcher: EventDispatcher | None = None,
    ) -> AsyncGenerator[ClientGroup, None]:
        """Create a set of clients only for a single token.

        Use this method if you want to run only one application with a single token.

        Args:
            token: Token to authenticate with Discord.
            session: Optional session to use for the clients.
            heartbeat_factory_type: Factory to create heartbeat clients.
            dispatcher: Event dispatcher to use for the clients.

        Returns:
            A set of clients to interact with Discord.
        """
        async with cls(session=session, heartbeat_factory_type=heartbeat_factory_type) as hub:
            yield hub.create_client_group('default', token, dispatcher)

    def create_client_group(
        self,
        group_name: str,
        token: str,
        dispatcher: EventDispatcher | None = None,
    ) -> ClientGroup:
        """Create a set of clients to interact with Discord.

        Args:
            group_name: Name of the set.
            token: Token to authenticate with Discord.
            dispatcher: Event dispatcher to use for the clients.

        Returns:
            A set of clients to interact with Discord.
        """
        if group_name in self.client_groups:
            raise ValueError(f'Client group {group_name} already exists')

        if dispatcher is None:
            dispatcher = self.event_dispatcher_type()

        client_group = self._build_client_group(group_name, token, dispatcher)

        dispatcher.add_argument('client', client_group.rest_client)
        dispatcher.add_argument('gateway', client_group.gateway_client)
        dispatcher.add_argument('client_groups', self.client_groups)

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
            await asyncio.gather(*tasks, return_exceptions=True)

    async def stop(self) -> None:
        """Stop the client hub."""
        for client in self.client_groups.values():
            await client.close()
        self.heartbeat_factory.stop()
        await self.session.close()
        logger.info(':wave: Shutdown complete', extra={'markup': True})

    async def __aenter__(self) -> Self:
        """Enter the context manager."""
        return self

    async def __aexit__(self, _exc_type, _exc, _tb) -> None:  # noqa: ANN001
        """Exit the context manager."""
        await self.start()

    def _build_client_group(
        self,
        group_name: str,
        token: str,
        event_dispatcher: EventDispatcher,
    ) -> ClientGroup:
        """Build a set of clients to interact with Discord.

        Args:
            group_name: Name of the set.
            token: Token to authenticate with Discord.
            event_dispatcher: Event dispatcher to use for the clients.

        Returns:
            A set of clients to interact with Discord.
        """
        middleware = BasicMiddleWare(
            headers={'Authorization': f'Bot {token}'},
            bucket_tracker=BucketTrack(),
        )
        http_client = AsyncHttpClient(session=self.session, middleware=middleware)
        rest_client = RestClient(token=token, http_client=http_client)
        gateway_client = GatewayClient(
            token=token,
            session=self.session,
            heartbeat_class=self.heartbeat_factory.create,
            dispatcher=event_dispatcher,
            name=group_name,
        )
        return ClientGroup(
            name=group_name,
            dispatcher=event_dispatcher,
            rest_client=rest_client,
            gateway_client=gateway_client,
        )


class ClientGroup(NamedTuple):
    """Group of clients.

    Include clients to interact with Discord.
    """

    name: str
    """Name of the set."""

    dispatcher: EventDispatcher
    """Event dispatcher."""

    rest_client: RestClient
    """Discord REST client."""

    gateway_client: GatewayClient
    """Discord gateway client."""

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
