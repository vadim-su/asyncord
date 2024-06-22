"""This module contains resource classes for interacting with messages."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.models.attachments import Attachment, make_payload_with_attachments
from asyncord.client.reactions.resources import ReactionResource
from asyncord.client.resources import APIResource
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.client.messages.models.requests.messages import CreateMessageRequest, UpdateMessageRequest
    from asyncord.snowflake import SnowflakeInputType

__ALL__ = ('MessageResource',)


class MessageResource(APIResource):
    """Resource to perform actions on messages.

    Attributes:
        channels_url: URL for the messages resource.
    """

    channels_url = REST_API_URL / 'channels'

    def __init__(self, http_client: HttpClient, channel_id: SnowflakeInputType) -> None:
        """Initialize the message resource."""
        super().__init__(http_client)
        self.channel_id = channel_id
        self.messages_url = self.channels_url / str(channel_id) / 'messages'

    def reactions(self, message_id: SnowflakeInputType) -> ReactionResource:
        """Get the reactions resource for a message.

        Args:
            message_id: ID of the message.

        Returns:
            Reactions resource for the message.
        """
        return ReactionResource(self._http_client, self.channel_id, message_id)

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

        resp = await self._http_client.get(url=url)
        return list_model(MessageResponse).validate_python(resp.body)

    async def create(self, message_data: CreateMessageRequest) -> MessageResponse:
        """Create a new message object for the channel.

        Args:
            message_data: Data to create the message with.

        Returns:
            Created message object.
        """
        url = self.messages_url
        attachments = cast(list[Attachment] | None, message_data.attachments)
        payload = make_payload_with_attachments(message_data, attachments=attachments)
        resp = await self._http_client.post(url=url, payload=payload)

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
        attachments = cast(list[Attachment] | None, message_data.attachments)
        payload = make_payload_with_attachments(message_data, attachments)
        resp = await self._http_client.patch(url=url, payload=payload)

        return MessageResponse(**resp.body)

    async def delete(self, message_id: SnowflakeInputType, reason: str | None = None) -> None:
        """Delete a message.

        Args:
            message_id: Id of the message.
            reason: Reason for deleting the message.
        """
        url = self.messages_url / str(message_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url=url, headers=headers)

    async def bulk_delete(
        self,
        message_ids: Sequence[SnowflakeInputType],
        reason: str | None = None,
    ) -> None:
        """Delete multiple messages.

        Args:
            message_ids: List of message ids to delete.
            reason: Reason for deleting the messages.
        """
        url = self.messages_url / 'bulk-delete'
        payload = {'messages': [str(message_id) for message_id in message_ids]}

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.post(url=url, payload=payload, headers=headers)

    async def crosspost_message(self, message_id: SnowflakeInputType) -> MessageResponse:
        """Crosspost a message in an Announcement channel to all channels following it.

        Reference:
        https://discord.com/developers/docs/resources/channel#crosspost-message

        Args:
            message_id: Id of the message to crosspost.

        Returns:
            Crossposted message object.
        """
        url = self.messages_url / str(message_id) / 'crosspost'

        resp = await self._http_client.post(url=url, payload={})
        return MessageResponse.model_validate(resp.body)

    async def get_pinned_messages(self, channel_id: SnowflakeInputType) -> list[MessageResponse]:
        """Get all pinned messages in a channel.

        Reference:
        https://discord.com/developers/docs/resources/channel#get-pinned-messages
        """
        url = self.channels_url / str(channel_id) / 'pins'

        resp = await self._http_client.get(url=url)
        return list_model(MessageResponse).validate_python(resp.body)

    async def pin_message(
        self,
        channel_id: SnowflakeInputType,
        message_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Pin a message in a channel.

        The max pinned messages is 50!

        Reference:
        https://discord.com/developers/docs/resources/channel#pin-message
        """
        url = self.channels_url / str(channel_id) / 'pins' / str(message_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = {}
        await self._http_client.put(url=url, payload=payload, headers=headers)

    async def unpin_message(
        self,
        channel_id: SnowflakeInputType,
        message_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Unpin a message in a channel.

        Reference:
        https://discord.com/developers/docs/resources/channel#unpin-message
        """
        url = self.channels_url / str(channel_id) / 'pins' / str(message_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url=url, headers=headers)
