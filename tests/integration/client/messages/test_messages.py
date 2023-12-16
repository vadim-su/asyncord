from __future__ import annotations

import random
import string

import pytest

from asyncord.client.messages import MessageResource
from asyncord.client.models.messages import CreateMessageData, Message, UpdateMessageData
from asyncord.client.rest import RestClient
from asyncord.typedefs import LikeSnowflake
from tests.conftest import IntegrationData

integrational_data = IntegrationData()


class TestMessages:
    @pytest.fixture()
    async def messages_res(
        self,
        client: RestClient,
        integration_data: IntegrationData,
    ):
        return client.channels.messages(integration_data.TEST_CHANNEL_ID)

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
            (integrational_data.TEST_MESSAGE_ID, None, None, 3),
            (None, integrational_data.TEST_MESSAGE_ID, None, 1),
            (None, None, integrational_data.TEST_MESSAGE_ID, 1),
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
