import random
import string
from typing import Literal

import pytest

from asyncord.client.messages import MessageResource
from asyncord.client.models.messages import CreateMessageData, Message, UpdateMessageData
from asyncord.typedefs import LikeSnowflake
from tests.conftest import IntegrationTestData


@pytest.mark.parametrize(
    'around,before,after,limit',
    [
        ('message_id', None, None, 3),
        (None, 'message_id', None, 1),
        (None, None, 'message_id', 1),
    ],
)
async def test_get_channel_messages(
    messages_res: MessageResource,
    integration_data: IntegrationTestData,
    around: LikeSnowflake | Literal['message_id'],
    before: LikeSnowflake | Literal['message_id'],
    after: LikeSnowflake | Literal['message_id'],
    limit: int,
):
    if around:
        around = integration_data.message_id
    if before:
        before = integration_data.message_id
    if after:
        after = integration_data.message_id

    messages = await messages_res.get(
        around=around, before=before, after=after, limit=limit,
    )
    assert len(messages) == limit
    if around:
        assert messages[1].id == around


async def test_create_and_delete_simple_message(messages_res: MessageResource):
    message = await messages_res.create(CreateMessageData(content='test'))
    assert message.content == 'test'
    await messages_res.delete(message.id)


async def test_update_message(message: Message, messages_res: MessageResource):
    random_content = ''.join([
        random.choice(string.ascii_letters)
        for _ in range(10)
    ])
    updated_message = await messages_res.update(
        message.id, UpdateMessageData(content=random_content),
    )
    assert updated_message.content == random_content
