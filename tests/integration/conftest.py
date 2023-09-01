import pytest

from asyncord.client.rest import RestClient


TEST_CHANNEL_ID = '920187645265608714'


@pytest.fixture()
async def client(token: str) -> RestClient:
    return RestClient(token)


@pytest.fixture()
async def messages_res(client: RestClient):
    return client.channels.messages(TEST_CHANNEL_ID)
