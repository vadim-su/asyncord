import pytest

from asyncord.client.rest import RestClient
from asyncord.client.messages import MessageResource
from asyncord.client.models.messages import CreateMessageData

TEST_CHANNEL_ID = '920187645265608714'


@pytest.fixture()
async def messages_res(client: RestClient):
    return client.channels.messages(TEST_CHANNEL_ID)


@pytest.fixture()
async def message(messages_res: MessageResource):
    message = await messages_res.create(
        CreateMessageData(content='test'),
    )
    yield message
    await messages_res.delete(message.id)
