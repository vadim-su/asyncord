from __future__ import annotations

import pytest

from asyncord.client.messages import MessageResource
from asyncord.client.models.messages import CreateMessageData, Message
from asyncord.client.reactions import ReactionResource
from asyncord.client.rest import RestClient
from tests.conftest import IntegrationData


class TestReactions:
    @pytest.fixture()
    async def messages_res(
        self,
        client: RestClient,
        integration_data: IntegrationData
    ):
        return client.channels.messages(integration_data.TEST_CHANNEL_ID)

    @pytest.fixture()
    async def message(self, messages_res: MessageResource):
        message = await messages_res.create(
            CreateMessageData(content='test'),
        )
        yield message
        await messages_res.delete(message.id)

    @pytest.fixture()
    async def reactions_res(self, message: Message, messages_res: MessageResource):
        return messages_res.reactions(message.id)

    async def test_add_and_get_reactions(
            self,
            reactions_res: ReactionResource,
            integration_data: IntegrationData
    ):
        test_emoji1 = '👍'
        test_emoji2 = '👎'

        await reactions_res.add(test_emoji1)
        await reactions_res.add(test_emoji2)

        assert (await reactions_res.get(test_emoji1))[0].id == integration_data.TEST_MEMBER_ID
        assert (await reactions_res.get(test_emoji2))[0].id == integration_data.TEST_MEMBER_ID

    async def test_delete_own_reaction(self, reactions_res: ReactionResource):
        test_emoji = '👍'
        await reactions_res.add(test_emoji)
        assert await reactions_res.get(test_emoji)

        await reactions_res.delete_own_reaction(test_emoji)
        assert not await reactions_res.get(test_emoji)

    async def test_delete_user_reaction(
        self,
        reactions_res: ReactionResource,
        integration_data: IntegrationData
    ):
        test_emoji = '👍'
        await reactions_res.add(test_emoji)
        assert await reactions_res.get(test_emoji)

        await reactions_res.delete(test_emoji, integration_data.TEST_MEMBER_ID)
        assert not await reactions_res.get(test_emoji)

    async def test_delete_all_reactions(self, reactions_res: ReactionResource):
        test_emoji1 = '👍'
        test_emoji2 = '👎'

        await reactions_res.add(test_emoji1)
        await reactions_res.add(test_emoji2)
        assert await reactions_res.get(test_emoji1)
        assert await reactions_res.get(test_emoji2)

        await reactions_res.delete()
        assert not await reactions_res.get(test_emoji1)
        assert not await reactions_res.get(test_emoji2)

    async def test_delete_all_reactions_for_emoji(self, reactions_res: ReactionResource):
        test_emoji1 = '👍'
        test_emoji2 = '👎'

        await reactions_res.add(test_emoji1)
        await reactions_res.add(test_emoji2)
        assert await reactions_res.get(test_emoji1)
        assert await reactions_res.get(test_emoji2)

        await reactions_res.delete(test_emoji1)
        assert not await reactions_res.get(test_emoji1)
        assert await reactions_res.get(test_emoji2)
