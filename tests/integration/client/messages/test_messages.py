import contextlib
import itertools
import random
import string
import warnings
from collections.abc import AsyncGenerator

import pytest

from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.http.errors import NotFoundError
from asyncord.client.messages.models.requests.messages import CreateMessageRequest, UpdateMessageRequest
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.messages.resources import MessageResource
from tests.conftest import IntegrationTestData


@pytest.fixture
async def multiple_messages(messages_res: MessageResource) -> AsyncGenerator[list[MessageResponse], None]:
    """Create multiple messages for testing bulk delete.

    In general, all messages must be deleted after the test is done. But we check it
    in the teardown fixture to make sure that the messages are deleted even if the test fails.
    """
    messages = []
    for _ in range(3):
        message = await messages_res.create(CreateMessageRequest(content='test'))
        messages.append(message)

    yield messages

    for message in messages:
        try:
            with contextlib.suppress(NotFoundError) as err:
                await messages_res.delete(message.id)
        except Exception as err:
            warnings.warn(f'Error deleting message: {err}', stacklevel=2)


@pytest.mark.parametrize(
    'limit',
    [None, 3],
)
@pytest.mark.parametrize(
    ('filter_name', 'filter_value'),
    [
        ('around', 'message_id'),
        ('before', 'message_id'),
        ('after', 'message_id'),
    ],
)
async def test_get_channel_messages_with_filter(
    filter_name: str,
    filter_value: str,
    limit: int,
    messages_res: MessageResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting messages from a channel with individual filters and a limit."""
    filter_value = getattr(integration_data, filter_value)

    messages = await messages_res.get(**{filter_name: filter_value, 'limit': limit})

    assert len(messages) > 0
    if limit:
        assert len(messages) <= limit

    message_ids = [message.id for message in messages]
    if filter_name == 'around':
        assert filter_value in message_ids
    else:
        assert filter_value not in message_ids


# Three filter combination
_three_filter_combination = [{'around': 'message_id', 'before': 'message_id', 'after': 'message_id'}]


@pytest.mark.parametrize(
    'limit',
    [None, 3],
)  # limit should not affect the test, but it's good to test it
@pytest.mark.parametrize(
    'filters',
    # Generate all unique combinations of filters without repetitions
    [
        {combo[0]: 'message_id', combo[1]: 'message_id', 'none': None}
        for combo in itertools.combinations(['around', 'before', 'after'], 2)
    ]
    + _three_filter_combination,
)
async def test_get_channel_messages_multiple_filters_error(
    limit: int,
    filters: dict,
    messages_res: MessageResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test that using more than one filter together raises a ValueError."""
    # Convert filter values from string to actual message ID from integration_data

    prepared_filters = {}
    for key in filters:  # noqa: PLC0206
        if filters[key] is None:
            continue
        prepared_filters[key] = getattr(integration_data, filters[key])

    with pytest.raises(ValueError, match='Only one of around, before, after can be specified'):
        await messages_res.get(**prepared_filters, limit=limit)


async def test_error_on_multiple_message_filters(messages_res: MessageResource) -> None:
    """Test that an error is raised when multiple filters are used."""
    with pytest.raises(
        ValueError,
        match='Only one of around, before, after can be specified',
    ):
        await messages_res.get(around=1, before=1)


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


async def test_bulk_delete_messages(
    multiple_messages: list[MessageResponse],
    messages_res: MessageResource,
) -> None:
    """Test bulk deleting messages."""
    message_ids = [message.id for message in multiple_messages]
    await messages_res.bulk_delete(message_ids)


async def test_crosspost_message(
    announcement_channel: ChannelResponse,
    channel_res: ChannelResource,
) -> None:
    """Test crossposting a message."""
    messages_res = channel_res.messages(announcement_channel.id)
    message = await messages_res.create(CreateMessageRequest(content='test'))

    crossposted_message = await messages_res.crosspost_message(message.id)

    messages = await messages_res.get(around=message.id, limit=10)
    assert crossposted_message.id in [msg.id for msg in messages]

    assert crossposted_message.id == message.id
    assert crossposted_message.content == message.content
