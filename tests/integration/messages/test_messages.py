from __future__ import annotations

import random
import string

import pytest

from asyncord.typedefs import LikeSnowflake
from asyncord.client.rest import RestClient
from asyncord.client.messages import MessageResource
from asyncord.client.models.messages import Message, CreateMessageData, UpdateMessageData

TEST_CHANNEL_ID = '920187645265608714'
TEST_MESSAGE_ID = '923584607427899402'
TEST_IMAGE_FILE = 'tests/data/test_image.jpg'


class TestMessages:
    @pytest.fixture()
    async def messages_res(self, client: RestClient):
        return client.channels.messages(TEST_CHANNEL_ID)

    @pytest.fixture()
    async def message(self, messages_res: MessageResource):
        message = await messages_res.create(
            CreateMessageData(content='test'),
        )
        yield message
        await messages_res.delete(message.id)

    @pytest.mark.parametrize(
        'around,before,after,limit',
        [
            (TEST_MESSAGE_ID, None, None, 3),
            (None, TEST_MESSAGE_ID, None, 1),
            (None, None, TEST_MESSAGE_ID, 1),
        ],
    )
    async def test_get_channel_messages(
        self,
        messages_res: MessageResource,
        around: LikeSnowflake,
        before: LikeSnowflake,
        after: LikeSnowflake,
        limit: int,
    ):
        messages = await messages_res.get(
            around=around, before=before, after=after, limit=limit,
        )
        assert len(messages) == limit
        if around:
            assert messages[1].id == around

    async def test_create_and_delete_simple_message(self, messages_res: MessageResource):
        message = await messages_res.create(CreateMessageData(content='test'))
        assert message.content == 'test'
        await messages_res.delete(message.id)

    async def test_update_message(self, message: Message, messages_res: MessageResource):
        random_content = ''.join([
            random.choice(string.ascii_letters)
            for _ in range(10)
        ])
        updated_message = await messages_res.update(
            message.id, UpdateMessageData(content=random_content),
        )
        assert updated_message.content == random_content