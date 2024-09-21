from unittest.mock import Mock

import aiohttp
import pytest
from pytest_mock import MockFixture

from asyncord.gateway.client.client import ConnectionData, GatewayClient
from asyncord.gateway.client.heartbeat import Heartbeat


@pytest.fixture
def gw_client(mocker: MockFixture) -> GatewayClient:
    """Create a GatewayClient instance."""
    return GatewayClient(
        token='token',  # noqa: S106
        session=Mock(spec=aiohttp.ClientSession),
        conn_data=ConnectionData(token='token'),  # noqa: S106
        heartbeat_class=Mock(spec=type(Heartbeat)),
    )
