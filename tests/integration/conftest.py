import pytest

from asyncord.client.rest import RestClient


@pytest.fixture()
async def client(token: str) -> RestClient:
    return RestClient(token)
