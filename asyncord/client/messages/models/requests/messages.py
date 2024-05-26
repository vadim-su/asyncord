"""This module contains message models.

Reference:
https://discord.com/developers/docs/resources/channel#message-object
"""

from __future__ import annotations

import io
import mimetypes
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Any, BinaryIO, Literal

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator, model_validator

from asyncord.client.messages.models.common import AllowedMentionType, AttachmentFlags, MessageFlags
from asyncord.client.messages.models.requests.components import (
    ActionRow,
    Component,
)
from asyncord.client.messages.models.requests.embeds import Embed
from asyncord.snowflake import SnowflakeInputType

MAX_COMPONENTS = 5
"""Maximum number of components in a message."""

MAX_EMBED_TEXT_LENGTH = 6000
"""Maximum length of the embed text."""

_OpennedFileType = io.BufferedReader | io.BufferedRandom
_AttachmentContentType = bytes | BinaryIO | _OpennedFileType
_FilePathType = str | Path
_AttachedFileInputType = Annotated[_FilePathType | _AttachmentContentType, _AttachmentContentType]


class AttachedFile(BaseModel, arbitrary_types_allowed=True):
    """Attached file.

    Arbitrary types are allowed because of the `content` field can be BinaryIO
    and other unsupported pydantic types.

    Reference:
    https://discord.com/developers/docs/resources/channel#attachment-object-attachment-structure
    """

    filename: str = None  # type: ignore
    """Name of attached file."""

    content_type: str = None  # type: ignore
    """Media type of the file."""

    content: _AttachedFileInputType
    """File content."""

    @model_validator(mode='before')
    def validate_file_info(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Fill filename and content type if not provided.

        Args:
            values: Values to validate.

        Returns:
            Validated values.
        """
        content = values.get('content')

        if not content:
            return values

        if isinstance(content, str):
            content = Path(content)

        # if file informaton is provided, skip other checks
        if values.get('filename') and values.get('content_type'):
            return values

        if isinstance(content, Path):
            content = content.open('rb')
            values['content'] = content
            if not values.get('filename'):
                values['filename'] = Path(content.name).name

        elif isinstance(content, BinaryIO | io.BufferedReader | io.BufferedRandom):
            if not values.get('filename'):
                values['filename'] = Path(content.name).name

        elif isinstance(content, bytes):
            if not values.get('filename'):
                raise ValueError("'filename' is required for bytes file")

        else:
            raise ValueError(f'Unsupported file object type: {type(content).__name__}')

        if not values.get('content_type'):
            content_type = mimetypes.guess_type(values['filename'])[0]
            if not content_type:
                raise ValueError(f"Unable to guess content type for {values['filename']}")

            values['content_type'] = content_type

        return values


_FilesListType = list[AttachedFile | _FilePathType | _OpennedFileType]
_FileMapType = Mapping[str | Path, _AttachmentContentType]
_FilesType = _FilesListType | _FileMapType


class AttachmentData(BaseModel):
    """Attachment object used for creating and editing messages.

    Reference:
    https://discord.com/developers/docs/resources/channel#attachment-object
    """

    id: SnowflakeInputType | int | None = None
    """Attachment ID."""

    filename: str | None = None
    """Name of the attached file."""

    description: str | None = Field(None, max_length=1024)
    """Description for the file.

    Max 1024 characters.
    """

    content_type: str | None = None
    """Media type of the file."""

    size: int | None = None
    """Size of the file in bytes."""

    url: AnyHttpUrl | None = None
    """Source URL of the file."""

    proxy_url: AnyHttpUrl | None = None
    """Proxied URL of the file."""

    height: int | None = None
    """Height of the file (if image)."""

    width: int | None = None
    """Width of the file (if image)."""

    ephemeral: bool | None = None
    """Whether this attachment is ephemeral.

    Ephemeral attachments will automatically be removed after a set period of time.
    Ephemeral attachments on messages are guaranteed to be available as long as
    the message itself exists.
    """

    duration_secs: float | None = None
    """Duration of the audio file (currently for voice messages)."""

    waveform: str | None = None
    """base64 encoded bytearray representing a sampled waveform.

    Currently for voice messages.
    """

    flags: AttachmentFlags | None = None
    """Attachment flags."""


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
            or values.get('files', False),
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

    @field_validator('files', mode='before', check_fields=False)
    def validate_attached_files(cls, files: _FilesType) -> list[AttachedFile]:
        """Prepare attached files.

        Args:
            files: Files to prepare.

        Returns:
            Prepared files to attach.
        """
        if not files:
            return []

        attached_files = files.items() if isinstance(files, Mapping) else files

        prepared_files = []

        for content in attached_files:
            match content:
                case AttachedFile():
                    prepared_files.append(content)

                # if list item - file_path or BinaryIO
                case str() | Path() | io.BufferedReader() | io.BufferedRandom() | BinaryIO():
                    prepared_files.append(AttachedFile(content=content))

                # if mapping item - filename, file
                case str() | Path() as filename, content if isinstance(content, _AttachmentContentType):
                    if isinstance(filename, Path):
                        filename = filename.name
                    prepared_files.append(
                        AttachedFile(filename=filename, content=content),
                    )

                case _:
                    raise ValueError('Invalid file object type')

        return prepared_files

    @field_validator('attachments', check_fields=False)
    def validate_attachments(cls, attachments: list[AttachmentData] | None) -> list[AttachmentData] | None:
        """Validate attachments.

        Args:
            attachments: Attachments to validate.

        Raises:
            ValueError: If attachments have mixed ids.

        Returns:
            Validated attachments.
        """
        if not attachments:
            return attachments

        attachment_id_exist_list = [attach.id is not None for attach in attachments]

        if all(attachment_id_exist_list):
            # Check is disabled because updated attachments already have id generated by Discord.
            # It means that after creating message with attachments all attachments will have Snowflake id.

            # for attachment in attachments:
            #     if attachment.id >= len(files):

            return attachments

        if any(attachment_id_exist_list):
            raise ValueError('Attachments must have all ids or none of them')

        for index, attachment in enumerate(attachments):
            attachment.id = index

        return attachments

    @field_validator('components', check_fields=False)
    def validate_components(cls, components: list[Component] | None) -> list[Component] | None:
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

        if not isinstance(components, list):
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

    content: str | None = Field(None, max_length=2000)
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

    components: list[Component] | Component | None = None
    """Components to include with the message."""

    sticker_ids: list[SnowflakeInputType] | None = None
    """Sticker ids to include with the message."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentData] | None = None
    """Attachment objects with filename and description.

    See Uploading Files:
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


class UpdateMessageRequest(BaseMessage):
    """Data to update a message with.

    Reference:
    https://discord.com/developers/docs/resources/channel#edit-message
    """

    content: str | None = Field(None, max_length=2000)
    """Message content."""

    embeds: list[Embed] | None = None
    """Embedded rich content."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions for the message."""

    components: list[Component] | Component | None = None
    """Components to include with the message."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentData] | None = None
    """Attachment objects with filename and description.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """
