import pytest

from asyncord.client.messages import MessageResource
from asyncord.client.models.messages import CreateMessageData


@pytest.fixture()
async def message(messages_res: MessageResource):
    message = await messages_res.create(
        CreateMessageData(content='test'),
    )
    yield message
    await messages_res.delete(message.id)
