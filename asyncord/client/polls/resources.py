"""This module contains the Polls resource.

For creating polls refer to messages resource.

Reference:
https://discord.com/developers/docs/resources/poll
"""

from asyncord.client.http.client import HttpClient
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.polls.models.responses import GetAnswerVotersResponse
from asyncord.client.resources import APIResource
from asyncord.snowflake import SnowflakeInputType
from asyncord.urls import REST_API_URL

__all__ = ('PollsResource',)


class PollsResource(APIResource):
    """Resource to perform actions on polls.

    Attributes:
        channels_url: URL for the messages resource.
    """

    channels_url = REST_API_URL / 'channels'

    def __init__(self, http_client: HttpClient, channel_id: SnowflakeInputType) -> None:
        """Initialize the polls resource."""
        super().__init__(http_client)
        self.channel_id = channel_id
        self.poll_url = self.channels_url / str(channel_id) / 'polls'

    async def get_answer_voters(
        self,
        message_id: SnowflakeInputType,
        answer_id: SnowflakeInputType,
        after: SnowflakeInputType | None = None,
        limit: int | None = None,
    ) -> GetAnswerVotersResponse:
        """Get a list of users that voted for this specific answer.

        Reference:
        https://discord.com/developers/docs/resources/poll#get-answer-voters

        Args:
            message_id: ID of the message.
            answer_id: ID of the answer.
            after: Get users after this user ID.
            limit: Max number of users to return (1-100). Defaut 25.
        """
        query_param = {}

        if after is not None:
            query_param['after'] = after
        if limit is not None:
            query_param['limit'] = limit

        url = self.poll_url / str(message_id) / 'answers' / str(answer_id) % query_param

        resp = await self._http_client.get(url=url)
        return GetAnswerVotersResponse.model_validate(resp.body)

    async def end_poll(self, message_id: SnowflakeInputType) -> MessageResponse:
        """Immediately end a poll.

        You can't end polls from other users.

        Reference:
        https://discord.com/developers/docs/resources/poll#end-poll

        Args:
            message_id: ID of the message.
        """
        url = self.poll_url / str(message_id) / 'expire'

        payload = {}

        resp = await self._http_client.post(url=url, payload=payload)
        return MessageResponse.model_validate(resp.body)
