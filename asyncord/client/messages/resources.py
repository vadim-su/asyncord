"""This module contains resource classes for interacting with messages."""

from __future__ import annotations

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.messages.models.requests.messages import CreateMessageRequest, UpdateMessageRequest
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.reactions.resources import ReactionResource
from asyncord.client.resources import ClientResource, ClientSubresource
from asyncord.snowflake import SnowflakeInputType
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL


class MessageResource(ClientSubresource):
    """Resource to perform actions on messages.

    Attributes:
        channels_url: URL for the messages resource.
    """

    channels_url = REST_API_URL / 'channels'

    def __init__(self, parent: ClientResource, channel_id: SnowflakeInputType) -> None:
        """Initialize the message resource."""
        super().__init__(parent)
        self.channel_id = channel_id
        self.messages_url = self.channels_url / str(channel_id) / 'messages'

    def reactions(self, message_id: SnowflakeInputType) -> ReactionResource:
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
        *,
        around: SnowflakeInputType | None = None,
        before: SnowflakeInputType | None = None,
        after: SnowflakeInputType | None = None,
        limit: int | None = None,
    ) -> list[MessageResponse]:
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

        url_params: dict[str, str | int] = {}
        if around is not None:
            url_params['around'] = str(around)
        if before is not None:
            url_params['before'] = str(before)
        if after is not None:
            url_params['after'] = str(after)
        if limit is not None:
            url_params['limit'] = limit

        url = self.messages_url % url_params

        resp = await self._http_client.get(url)
        return list_model(MessageResponse).validate_python(resp.body)

    async def create(self, message_data: CreateMessageRequest) -> MessageResponse:
        """Create a new message object for the channel.

        Args:
            message_data: Data to create the message with.

        Returns:
            Created message object.
        """
        url = self.messages_url
        payload = message_data.model_dump(mode='json', exclude_unset=True)

        # fmt: off
        resp = await self._http_client.post(
            url=url,
            payload=payload,
            files=[(file.filename, file.content_type, file.content) for file in message_data.files],
        )
        # fmt: on

        return MessageResponse.model_validate(resp.body)

    async def update(self, message_id: SnowflakeInputType, message_data: UpdateMessageRequest) -> MessageResponse:
        """Update a message.

        Args:
            message_id: Id of the message.
            message_data: Data to update the message with.

        Returns:
            Updated message object.
        """
        url = self.messages_url / str(message_id)
        payload = message_data.model_dump(mode='json', exclude_unset=True)

        # fmt: off
        resp = await self._http_client.patch(
            url=url,
            payload=payload,
            files=[(file.filename, file.content_type, file.content) for file in message_data.files],
        )
        # fmt: on

        return MessageResponse(**resp.body)

    async def delete(self, message_id: SnowflakeInputType, reason: str | None = None) -> None:
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

        await self._http_client.delete(url, headers=headers)

    async def bulk_delete(
        self,
        message_ids: list[SnowflakeInputType],
        reason: str | None = None,
    ) -> None:
        """Delete multiple messages.

        Args:
            message_ids: List of message ids to delete.
            reason: Reason for deleting the messages.
        """
        url = self.messages_url / 'bulk-delete'
        payload = {'messages': [str(message_id) for message_id in message_ids]}

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.post(url, payload, headers=headers)
