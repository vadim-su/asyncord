from typing import Any, AsyncGenerator

import aiohttp
import pytest

from asyncord.client.rest import RestClient
from asyncord.gateway.client import GatewayClient
from tests.conftest import IntegrationData


@pytest.fixture()
async def client(token: str) -> RestClient:
    return RestClient(token)


@pytest.fixture()
async def gateway(client: RestClient, token: str) -> AsyncGenerator[GatewayClient, Any]:
    async with aiohttp.ClientSession() as session:
        gw = GatewayClient(token, session=session)
        client = RestClient(token)
        client._http._session = session
        gw.dispatcher.add_argument('client', client)
        yield gw


@pytest.fixture()
async def messages_res(client: RestClient, integration_data: IntegrationData):
    return client.channels.messages(IntegrationData.TEST_CHANNEL_ID)
