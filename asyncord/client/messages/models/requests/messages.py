"""This module contains message models.

Reference:
https://discord.com/developers/docs/resources/message#message-object
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    Field,
)

from asyncord.client.messages.models.common import AllowedMentionType, MessageFlags
from asyncord.client.messages.models.requests.base_message import BaseMessage, ListAttachmentType, SingleAttachmentType
from asyncord.client.messages.models.requests.components import MessageComponentType
from asyncord.client.messages.models.requests.embeds import Embed
from asyncord.client.polls.models.requests import Poll
from asyncord.snowflake import SnowflakeInputType

__ALL__ = (
    'AllowedMentions',
    'MessageReference',
    'CreateMessageRequest',
    'UpdateMessageRequest',
)


class AllowedMentions(BaseModel):
    """Allowed mentions object.

    Reference:
    https://discord.com/developers/docs/resources/message#allowed-mentions-object
    """

    parse: list[AllowedMentionType] | None = None
    """Array of allowed mention types to parse from the content."""

    roles: Annotated[list[SnowflakeInputType], Field(max_length=100)] | None = None
    """Array of role IDs to mention."""

    users: Annotated[list[SnowflakeInputType], Field(max_length=100)] | None = None
    """Array of user IDs to mention."""

    replied_user: bool | None = None
    """For replies, whether to mention the author of the message being replied to."""


class MessageReference(BaseModel):
    """Message reference object used for creating messages.

    Reference:
    https://discord.com/developers/docs/resources/message#message-reference-object
    """

    message_id: SnowflakeInputType | None = None
    """ID of the originating message."""

    channel_id: SnowflakeInputType | None = None
    """ID of the originating message's channel."""

    guild_id: SnowflakeInputType | None = None
    """ID of the originating message's guild."""

    fail_if_not_exists: bool | None = None
    """Flag to tell the API to return an error object instead.

    When sending a message that references another message, this field determines
    whether to error if the referenced message doesn't exist instead of sending
    the message as a normal (non-reply) message.

    If None is set, the default serverside value is True.
    """


class CreateMessageRequest(BaseMessage):
    """Data to create a message with.

    Reference:
    https://discord.com/developers/docs/resources/message#create-message
    """

    content: Annotated[str | None, Field(max_length=2000)] = None
    """Message content."""

    nonce: Annotated[str, Field(max_length=25)] | int | None = None
    """Can be used to verify a message was sent.

    Value will appear in the Message Create event.
    """

    tts: bool | None = None
    """True if this is a TTS message."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions for the message."""

    message_reference: MessageReference | None = None
    """Reference data sent with crossposted messages."""

    components: Sequence[MessageComponentType] | MessageComponentType | None = None
    """Components to include with the message."""

    sticker_ids: list[SnowflakeInputType] | None = None
    """Sticker ids to include with the message."""

    attachments: Annotated[
        ListAttachmentType | SingleAttachmentType | None,
        Field(validate_default=True),  # Necessary for the embedded attachment collection
    ] = None
    """List of attachment object.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS, MessageFlags.SUPPRESS_NOTIFICATIONS] | None = None
    """The flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    enforce_nonce: bool = True
    """Ensures a nonce is unique.

    Returns an existing message with the same nonce and author instead of creating a new one.
    I set it to True because it will be default behavior in the near future.
    """

    poll: Poll | None = None
    """A poll."""


class UpdateMessageRequest(BaseMessage):
    """Data to update a message with.

    Reference:
    https://discord.com/developers/docs/resources/message#edit-message
    """

    content: Annotated[str | None, Field(max_length=2000)] = None
    """Message content."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions for the message."""

    components: Sequence[MessageComponentType] | MessageComponentType | None = None
    """Components to include with the message."""

    attachments: Annotated[
        ListAttachmentType | SingleAttachmentType | None,
        Field(validate_default=True),  # Necessary for the embedded attachment collection
    ] = None
    """List of attachment object.

    You can set this to any bytes-like object, a file-like object, or a path-like object.
    Of course, you can also set it to an Attachment object and list of any of the above.
    Full allowed types defined in `_SingleAttachmentType`.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """
