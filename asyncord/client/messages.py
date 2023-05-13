from __future__ import annotations

from asyncord.urls import REST_API_URL
from asyncord.typedefs import LikeSnowflake
from asyncord.client.reactions import ReactionResource
from asyncord.client.resources import ClientResource, ClientSubresources
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.models.messages import Message, CreateMessageData, UpdateMessageData


class MessageResource(ClientSubresources):
    """Resource to perform actions on messages.

    Attributes:
        channel_id (LikeSnowflake): The ID of the channel.
        messages_url (URL): The URL for the messages resource.
    """

    channels_url = REST_API_URL / 'channels'

    def __init__(self, parent: ClientResource, channel_id: LikeSnowflake):
        super().__init__(parent)
        self.channel_id = channel_id
        self.messages_url = self.channels_url / str(channel_id) / 'messages'

    def reactions(self, message_id: LikeSnowflake) -> ReactionResource:
        """Get the reactions resource for a message.

        Args:
            channel_id (LikeSnowflake): The ID of the channel.
            message_id (LikeSnowflake): The ID of the message.

        Returns:
            ReactionsResource: The reactions resource for the message.
        """
        return ReactionResource(self, self.channel_id, message_id)

    async def get(
        self,
        around: LikeSnowflake | None = None,
        before: LikeSnowflake | None = None,
        after: LikeSnowflake | None = None,
        limit: int | None = None,
    ) -> list[Message]:
        """Get the messages for a channel.

        Args:
            around (LikeSnowflake | None): Get messages around this message ID.
            before (LikeSnowflake | None): Get messages before this message ID.
            after (LikeSnowflake | None): Get messages after this message ID.
            limit (int | None): The maximum number of messages to return (1-100).

        Returns:
            list[Channel]: A list of message objects.
        """
        if bool(around) + bool(before) + bool(after) > 1:
            raise ValueError('Only one of around, before, after can be specified.')

        url_params = {}
        if around is not None:
            url_params['around'] = str(around)
        if before is not None:
            url_params['before'] = str(before)
        if after is not None:
            url_params['after'] = str(after)
        if limit is not None:
            url_params['limit'] = limit

        url = self.messages_url % url_params

        resp = await self._http.get(url)
        return [Message(**message) for message in resp.body]

    async def create(self, message_data: CreateMessageData) -> Message:
        """Create a new message object for the channel.

        Args:
            message_data (CreateMessageData): Data to create the message with.

        Returns:
            Message: Created message object.
        """
        url = self.messages_url
        payload = message_data.dict(exclude_unset=True)
        resp = await self._http.post(
            url=url,
            payload=payload,
            files=[
                (file.filename, file.content_type, file.content)
                for file in message_data.files
            ],
        )

        return Message(**resp.body)

    async def update(self, message_id: LikeSnowflake, message_data: UpdateMessageData) -> Message:
        """Update a message.

        Args:
            message_id (LikeSnowflake): Id of the message.
            message_data (UpdateMessageData): Data to update the message with.

        Returns:
            Message: Updated message object.
        """
        url = self.messages_url / str(message_id)
        payload = message_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http.patch(
            url=url,
            payload=payload,
            files=[
                (file.filename, file.content_type, file.content)
                for file in message_data.files
            ],
        )
        return Message(**resp.body)

    async def delete(self, message_id: LikeSnowflake, reason: str | None = None) -> None:
        """Delete a message.

        Args:
            message_id (LikeSnowflake): Id of the message.
            reason (str | None): Reason for deleting the message.
        """
        url = self.messages_url / str(message_id)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http.delete(url, headers=headers)
