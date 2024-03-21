"""This module contains the client hub to process multiple clients."""

# TODO: Add example usage of the client hub.
import asyncio
import logging
from typing import NamedTuple

import aiohttp

from asyncord.client.http.client import AsyncHttpClient
from asyncord.client.rest import RestClient
from asyncord.gateway.client.client import GatewayClient
from asyncord.gateway.client.heartbeat import HeartbeatFactory
from asyncord.gateway.dispatcher import EventDispatcher

logger = logging.getLogger(__name__)


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


class ClientHub:
    """Hub to process multiple clients."""

    def __init__(self) -> None:
        """Initialize hub to process multiple clients."""
        self.session: aiohttp.ClientSession
        self.heartbeat_factory = HeartbeatFactory()
        self.client_groups: dict[str, ClientGroup] = {}

    def create_clients(self, group_name: str, token: str) -> ClientGroup:
        """Create a set of clients to interact with Discord."""
        http_client = AsyncHttpClient(
            session=self.session,
            headers={'Authorization': f'Bot {token}'},
        )
        rest_client = RestClient(token=token, http_client=http_client)

        dispatcher = EventDispatcher()
        gateway_client = GatewayClient(
            token=token,
            session=self.session,
            heartbeat_class=self.heartbeat_factory.create,
            dispatcher=dispatcher,
            name=group_name,
        )
        dispatcher.add_argument('client', rest_client)
        dispatcher.add_argument('gateway', gateway_client)
        dispatcher.add_argument('clients', self.client_groups)

        client_set = ClientGroup(
            name=group_name,
            dispatcher=dispatcher,
            rest_client=rest_client,
            gateway_client=gateway_client,
        )

        self.client_groups[group_name] = client_set

        return client_set

    async def run(self) -> None:
        """Run client hub to process multiple clients.

        When the hub is running, it will connect to the Discord clients and process the events.
        """
        logger.info(':satellite: Connecting to Discord', extra={'markup': True})
        tasks = [client.connect() for client in self.client_groups.values()]
        try:
            await asyncio.gather(*tasks)
        except (KeyboardInterrupt, asyncio.CancelledError):
            logger.info('Shutting down...')
            await asyncio.gather(*tasks, return_exceptions=True)

    async def __aexit__(self, _exc_type, _exc, _tb) -> None:  # noqa: ANN001
        """Exit the context manager."""
        for client in self.client_groups.values():
            await client.close()
        self.heartbeat_factory.stop()
        await self.session.close()
        logger.info(':wave: Shutdown complete', extra={'markup': True})