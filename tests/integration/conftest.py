from typing import Any, AsyncGenerator
import aiohttp
import pytest

from asyncord.client.rest import RestClient
from asyncord.gateway.client import GatewayClient


TEST_CHANNEL_ID = '920187645265608714'
TEST_VOICE_CHANNEL_ID = '1157605385826476062'
TEST_GUILD_ID = '763522265874694144'


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
async def messages_res(client: RestClient):
    return client.channels.messages(TEST_CHANNEL_ID)


@pytest.fixture()
def guild_id() -> str:
    return TEST_GUILD_ID


@pytest.fixture()
def channel_id() -> str:
    return TEST_CHANNEL_ID


@pytest.fixture()
def voice_channel_id() -> str:
    return TEST_VOICE_CHANNEL_ID
