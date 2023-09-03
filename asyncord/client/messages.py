"""This module contains resource classes for interacting with messages."""

from __future__ import annotations

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.models.messages import CreateMessageData, Message, UpdateMessageData
from asyncord.client.reactions import ReactionResource
from asyncord.client.resources import ClientResource, ClientSubresources
from asyncord.typedefs import LikeSnowflake, list_model
from asyncord.urls import REST_API_URL


class MessageResource(ClientSubresources):
    """Resource to perform actions on messages.

    Attributes:
        channels_url: URL for the messages resource.
    """

    channels_url = REST_API_URL / 'channels'

    def __init__(self, parent: ClientResource, channel_id: LikeSnowflake):
        """Initialize the message resource."""
        super().__init__(parent)
        self.channel_id = channel_id
        self.messages_url = self.channels_url / str(channel_id) / 'messages'

    def reactions(self, message_id: LikeSnowflake) -> ReactionResource:
        """Get the reactions resource for a message.

        Args:
            channel_id: ID of the channel.
            message_id: ID of the message.

        Returns:
            Reactions resource for the message.
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
            around: Get messages around this message ID.
            before: Get messages before this message ID.
            after: Get messages after this message ID.
            limit: Maximum number of messages to return (1-100).

        Returns:
            List of message objects.
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
        return list_model(Message).validate_python(resp.body)

    async def create(self, message_data: CreateMessageData) -> Message:
        """Create a new message object for the channel.

        Args:
            message_data: Data to create the message with.

        Returns:
            Created message object.
        """
        url = self.messages_url
        payload = message_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http.post(
            url=url,
            payload=payload,
            files=[
                (file.filename, file.content_type, file.content)
                for file in message_data.files
            ],
        )

        return Message.model_validate(resp.body)

    async def update(self, message_id: LikeSnowflake, message_data: UpdateMessageData) -> Message:
        """Update a message.

        Args:
            message_id: Id of the message.
            message_data: Data to update the message with.

        Returns:
            Updated message object.
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
            message_id: Id of the message.
            reason: Reason for deleting the message.
        """
        url = self.messages_url / str(message_id)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http.delete(url, headers=headers)
