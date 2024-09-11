"""Contains tests for polls resource."""

from collections.abc import AsyncGenerator

import pytest

from asyncord.client.messages.models.requests.messages import CreateMessageRequest
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.messages.resources import MessageResource
from asyncord.client.polls.models.common import PollLayoutType
from asyncord.client.polls.models.requests import Answer, Poll, PollEmoji
from asyncord.client.polls.resources import PollsResource


@pytest.fixture
async def poll_message(messages_res: MessageResource) -> AsyncGenerator[MessageResponse, None]:
    """Create a message with a poll.

    After the test, delete the message.
    """
    message_with_poll = CreateMessageRequest(
        content='test',
        poll=Poll(
            question='test?',
            answers=[
                Answer(
                    text='test',
                ),
                Answer(
                    text='test',
                    emoji=PollEmoji(
                        name='👍',
                    ),
                ),
            ],
            allow_multiselect=True,
            layout_type=PollLayoutType.DEFAULT,
        ),
    )
    message = await messages_res.create(message_with_poll)
    yield message
    await messages_res.delete(message.id)


async def test_create_and_delete_message_with_poll(poll_message: MessageResponse) -> None:
    """Test creating and deleting a message with a poll."""
    poll = poll_message.poll

    assert poll
    assert poll.question == 'test?'
    assert len(poll.answers) == 2

    answers = poll.answers
    assert answers[0].answer_id
    assert answers[0].poll_media.text

    assert answers[1].answer_id
    assert answers[1].poll_media.emoji
    assert answers[1].poll_media.emoji.name == '👍'

    assert poll.expiry


@pytest.mark.parametrize('after', [None, 10])
@pytest.mark.parametrize('limit', [None, 10])
async def test_get_voters_for_answer(
    after: int | None,
    limit: int | None,
    poll_message: MessageResponse,
    polls_res: PollsResource,
) -> None:
    """Test getting voters for an answer."""
    poll = poll_message.poll
    assert poll

    answer_id = poll.answers[0].answer_id

    voters = await polls_res.get_answer_voters(
        message_id=poll_message.id,
        answer_id=answer_id,
        after=after,
        limit=limit,
    )
    assert not voters.users


async def test_end_poll(poll_message: MessageResponse, polls_res: PollsResource) -> None:
    """Test ending a poll."""
    poll = poll_message.poll
    assert poll

    await polls_res.end_poll(message_id=poll_message.id)

    # We doesn't check finalization because it's not guaranteed that the poll
    # will be finalized after ending.
    # Read how to pool working at: https://discord.com/developers/docs/resources/poll#poll-results-object


async def test_poll_emoji_cant_contain_id_and_name() -> None:
    """Test that a poll emoji can't contain an id and a name at the same time."""
    with pytest.raises(ValueError, match='Only one of id or name'):
        PollEmoji(
            name='👍',
            id=123,
        )


async def test_poll_emoji_must_contain_id_or_name() -> None:
    """Test that a poll emoji must contain an id or a name."""
    with pytest.raises(ValueError, match='Either id or name must be set'):
        PollEmoji()
