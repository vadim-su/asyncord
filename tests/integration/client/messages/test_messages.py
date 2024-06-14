import random
import string
from typing import Literal

import pytest

from asyncord.client.messages.models.requests.messages import CreateMessageRequest, UpdateMessageRequest
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.messages.resources import MessageResource
from asyncord.snowflake import SnowflakeInputType
from tests.conftest import IntegrationTestData


@pytest.mark.parametrize(
    ('around', 'before', 'after', 'limit'),
    [
        ('message_id', None, None, 3),
        (None, 'message_id', None, 1),
        (None, None, 'message_id', 1),
    ],
)
async def test_get_channel_messages(
    messages_res: MessageResource,
    integration_data: IntegrationTestData,
    around: SnowflakeInputType | Literal['message_id'],
    before: SnowflakeInputType | Literal['message_id'],
    after: SnowflakeInputType | Literal['message_id'],
    limit: int,
) -> None:
    """Test getting messages from a channel."""
    if around:
        around = integration_data.message_id
    if before:
        before = integration_data.message_id
    if after:
        after = integration_data.message_id

    messages = await messages_res.get(
        around=around,
        before=before,
        after=after,
        limit=limit,
    )
    assert len(messages) == limit
    if around:
        assert messages[1].id == around


async def test_create_and_delete_simple_message(messages_res: MessageResource) -> None:
    """Test creating and deleting a message."""
    message = await messages_res.create(CreateMessageRequest(content='test'))
    assert message.content == 'test'
    await messages_res.delete(message.id)


async def test_update_message(
    message: MessageResponse,
    messages_res: MessageResource,
) -> None:
    """Test updating a message."""
    # fmt: off
    random_content = ''.join([
        random.choice(string.ascii_letters)
        for _ in range(10)
    ])
    # fmt: on
    updated_message = await messages_res.update(
        message.id,
        UpdateMessageRequest(content=random_content),
    )
    assert updated_message.content == random_content


async def test_message_pin_unpin_flow(
    message: MessageResponse,
    integration_data: IntegrationTestData,
    messages_res: MessageResource,
) -> None:
    """Test the flow of pinning, getting, and unpinning a message."""
    # Check initial state
    initial_pins = await messages_res.get_pinned_messages(integration_data.channel_id)
    assert message.id not in [msg.id for msg in initial_pins]

    # Pin the message
    await messages_res.pin_message(integration_data.channel_id, message.id)

    # Check that the message is pinned
    pins_after_pin = await messages_res.get_pinned_messages(integration_data.channel_id)
    assert message.id in [msg.id for msg in pins_after_pin]

    # Unpin the message
    await messages_res.unpin_message(integration_data.channel_id, message.id)

    # Check that the message is no longer pinned
    pins_after_unpin = await messages_res.get_pinned_messages(integration_data.channel_id)
    assert message.id not in [msg.id for msg in pins_after_unpin]
