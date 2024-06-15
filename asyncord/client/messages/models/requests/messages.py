"""This module contains message models.

Reference:
https://discord.com/developers/docs/resources/channel#message-object
"""

from __future__ import annotations

from collections.abc import Sequence
from io import BufferedReader, IOBase
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    Field,
    SerializerFunctionWrapHandler,
    field_serializer,
    field_validator,
    model_validator,
)

from asyncord.client.messages.models.common import AllowedMentionType, MessageFlags
from asyncord.client.messages.models.requests.components import ActionRow, Component
from asyncord.client.messages.models.requests.embeds import Embed
from asyncord.client.models.attachments import Attachment, AttachmentContentType
from asyncord.client.polls.models.requests import PollRequest
from asyncord.snowflake import SnowflakeInputType

__ALL__ = (
    'BaseMessage',
    'AllowedMentions',
    'MessageReference',
    'CreateMessageRequest',
    'UpdateMessageRequest',
)

MAX_COMPONENTS = 5
"""Maximum number of components in a message."""

MAX_EMBED_TEXT_LENGTH = 6000
"""Maximum length of the embed text."""


class BaseMessage(BaseModel):
    """Base message data class used for message creation and editing.

    Contains axillary validation methods.
    """

    @model_validator(mode='before')
    def has_any_content(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate message content.

        Reference:
        https://discord.com/developers/docs/resources/channel#message-object-message-structure

        Args:
            values: Values to validate.

        Returns:
            Validated values.

        Raises:
            ValueError: If the message has no content or embeds.
        """
        has_any_content = bool(
            values.get('content', False)
            or values.get('embeds', False)
            or values.get('sticker_ids', False)
            or values.get('components', False)
            or values.get('attachments', False),
        )

        if not has_any_content:
            raise ValueError(
                'Message must have content, embeds, stickers, components or files.',
            )

        return values

    @field_validator('embeds', check_fields=False)
    def validate_embeds(cls, embeds: list[Embed] | None) -> list[Embed] | None:
        """Check total embed text length.

        Reference:
        https://discord.com/developers/docs/resources/channel#message-object-message-structure

        Args:
            embeds: Values to validate.

        Raises:
            ValueError: If the total embed text length is more than 6000 characters.

        Returns:
            Validated values.
        """
        if not embeds:
            return embeds

        total_embed_text_length = 0
        for embed in embeds:
            total_embed_text_length += cls._embed_text_length(embed)

            if total_embed_text_length > MAX_EMBED_TEXT_LENGTH:
                raise ValueError(
                    'Total embed text length must be less than 6000 characters.',
                )

        return embeds

    @field_validator('attachments', mode='before', check_fields=False)
    def convert_files_to_attachments(
        cls,
        attachments: Sequence[Attachment | AttachmentContentType],
    ) -> list[Attachment]:
        """Convert files to attachments.

        Args:
            attachments: Attachments to convert.

        Returns:
            Converted attachments.
        """
        converted_attachments = []
        for index, attachment in enumerate(attachments):
            match attachment:
                case Attachment():
                    converted_attachments.append(attachment)

                case bytes() | bytearray() | memoryview() | BufferedReader() | IOBase() | Path():
                    converted_attachments.append(Attachment(id=index, content=attachment))

                case _:
                    raise ValueError(f'Invalid attachment type: {type(attachment)}')

        return converted_attachments

    @field_validator('attachments', check_fields=False)
    def validate_attachments(cls, attachments: list[Attachment] | None) -> list[Attachment] | None:
        """Validate attachments.

        Args:
            attachments: Attachments to validate.

        Raises:
            ValueError: If attachments have mixed ids.
                All attachments must have ids or none of them.

        Returns:
            Validated attachments.
        """
        if not attachments:
            return attachments

        attachment_ids_is_not_none = [attach.id is not None for attach in attachments]

        if any(attachment_ids_is_not_none) and not all(attachment_ids_is_not_none):
            raise ValueError('Attachments must have all ids or none of them')

        for index, attachment in enumerate(attachments):
            if attachment.do_not_attach and not attachment.content:
                raise ValueError('Do not attach attachments must have content')

            if attachment.id is None:
                attachment.id = index

        return attachments

    @field_serializer('attachments', mode='wrap', when_used='json-unless-none', check_fields=False)
    @classmethod
    def serialize_attachments(
        cls,
        attachments: list[Attachment] | None,
        next_serializer: SerializerFunctionWrapHandler,
    ) -> list[dict[str, Any]] | None:
        """Serialize attachments.

        Args:
            attachments: Attachments to serialize.
            next_serializer: Next serializer in the chain.

        Returns:
            Serialized attachments.
        """
        if attachments is None:
            return next_serializer(attachments)

        # fmt: off
        attachments = [
            attachment
            for attachment in attachments
            if not attachment.do_not_attach
        ]
        # fmt: on

        return next_serializer(attachments)

    @field_validator('components', check_fields=False)
    def validate_components(cls, components: Sequence[Component] | Component | None) -> Sequence[Component] | None:
        """Validate components.

        Args:
            components: Components to validate.

        Raises:
            ValueError: If components have more than 5 action rows or are not wrapped in an ActionRow.

        Returns:
            Validated components.
        """
        if not components:
            return components

        if not isinstance(components, Sequence):
            components = [components]

        if len(components) > MAX_COMPONENTS:
            raise ValueError('Components must have 5 or fewer action rows')

        if all(isinstance(component, ActionRow) for component in components):
            return components

        if all(not isinstance(component, ActionRow) for component in components):
            return [ActionRow(components=components)]

        raise ValueError(
            "All components must be wrapped on an ActionRow or don't wrap them at all",
        )

    @classmethod
    def _embed_text_length(cls, embed: Embed) -> int:
        """Get the length of the embed text.

        Args:
            embed: Embed to get the length of.

        Returns:
            Length of the embed text.
        """
        embed_text_length = len(embed.title or '')
        embed_text_length += len(embed.description or '')

        if embed.footer:
            embed_text_length += len(embed.footer.text)

        if embed.author:
            embed_text_length += len(embed.author.name)

        for field in embed.fields:
            embed_text_length += len(field.name)
            embed_text_length += len(field.value)

        return embed_text_length


class AllowedMentions(BaseModel):
    """Allowed mentions object.

    Reference:
    https://discord.com/developers/docs/resources/channel#allowed-mentions-object
    """

    parse: list[AllowedMentionType] | None = None
    """Array of allowed mention types to parse from the content."""

    roles: list[SnowflakeInputType] | None = Field(None, max_length=100)
    """Array of role IDs to mention."""

    users: list[SnowflakeInputType] | None = Field(None, max_length=100)
    """Array of user IDs to mention."""

    replied_user: bool | None = None
    """For replies, whether to mention the author of the message being replied to."""


class MessageReference(BaseModel):
    """Message reference object used for creating messages.

    Reference:
    https://discord.com/developers/docs/resources/channel#message-reference-object
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
    https://discord.com/developers/docs/resources/channel#create-message
    """

    content: Annotated[str | None, Field(max_length=2000)] = None
    """Message content."""

    nonce: Annotated[str, Field(max_length=25)] | int | None = None
    """Can be used to verify a message was sent.

    Value will appear in the Message Create event.
    """

    tts: bool | None = None
    """True if this is a TTS message."""

    embeds: list[Embed] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions for the message."""

    message_reference: MessageReference | None = None
    """Reference data sent with crossposted messages."""

    components: Sequence[Component] | Component | None = None
    """Components to include with the message."""

    sticker_ids: list[SnowflakeInputType] | None = None
    """Sticker ids to include with the message."""

    attachments: list[Annotated[Attachment | AttachmentContentType, Attachment]] | None = None
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

    poll: PollRequest | None = None
    """A poll."""


class UpdateMessageRequest(BaseMessage):
    """Data to update a message with.

    Reference:
    https://discord.com/developers/docs/resources/channel#edit-message
    """

    content: Annotated[str | None, Field(max_length=2000)] = None
    """Message content."""

    embeds: list[Embed] | None = None
    """Embedded rich content."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions for the message."""

    components: Sequence[Component] | Component | None = None
    """Components to include with the message."""

    attachments: Sequence[Annotated[Attachment | AttachmentContentType, Attachment]] | None = None
    """List of attachment object.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """
