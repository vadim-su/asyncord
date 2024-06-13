"""Contains tests for polls resource."""

from asyncord.client.messages.models.requests.messages import CreateMessageRequest
from asyncord.client.messages.resources import MessageResource
from asyncord.client.polls.models.common import PollLayoutType
from asyncord.client.polls.models.requests import PollAnswer, PollMedia, PollRequest
from asyncord.client.polls.resources import PollsResource


# FIXME: The DISCORD API doesn't return answer_id.
# I don't know how to test PollsReqource.get_answer_voters() without it.
async def test_create_and_delete_poll(
    messages_res: MessageResource,
    polls_res: PollsResource,
) -> None:
    """Test creating and deleting a message."""
    message = await messages_res.create(
        CreateMessageRequest(
            content='test',
            poll=PollRequest(
                question=PollMedia(
                    text='test?',
                ),
                answers=[
                    PollAnswer(
                        poll_media=PollMedia(
                            text='test',
                        ),
                    ),
                    PollAnswer(
                        poll_media=PollMedia(
                            text='test',
                        ),
                    ),
                ],
                allow_multiselect=True,
                layout_type=PollLayoutType.DEFAULT,
            ),
        ),
    )

    await polls_res.end_poll(message.id)

    assert message.poll
    await messages_res.delete(message.id)
