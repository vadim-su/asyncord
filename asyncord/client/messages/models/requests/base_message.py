"""This module defines the `BaseMessage` class, which is used for creating and editing messages.

It includes auxiliary validation methods to ensure the integrity and correctness of message data.
"""

from collections.abc import Sequence
from typing import Annotated, Any, Final, Self

from pydantic import (
    BaseModel,
    Field,
    SerializerFunctionWrapHandler,
    ValidationInfo,
    field_serializer,
    field_validator,
    model_validator,
)

from asyncord.client.messages.models.requests.components.action_row import ActionRow, MessageComponentType
from asyncord.client.messages.models.requests.embeds import Embed, EmbedImage
from asyncord.client.models.attachments import Attachment, AttachmentContentType, get_content_type
from asyncord.snowflake import SnowflakeInputType

__all__ = (
    'MAX_COMPONENTS',
    'MAX_EMBED_TEXT_LENGTH',
    'BaseMessage',
    'ListAttachmentType',
    'SingleAttachmentType',
)

MAX_COMPONENTS: Final[int] = 5
"""Maximum number of components in a message."""

MAX_EMBED_TEXT_LENGTH: Final[int] = 6000
"""Maximum length of the embed text."""

_EMBED_ATTACHMENT_DATA_FIELD: Final[str] = '__embed_attachments'
"""Data field name for the embed attachments data."""


SingleAttachmentType = Annotated[Attachment | AttachmentContentType, Attachment]
"""Single message attachment type."""

ListAttachmentType = Annotated[Sequence[SingleAttachmentType], Sequence[Attachment]]
"""List of message attachments type."""


class BaseMessage(BaseModel):
    """Base message data class used for message creation and editing.

    Contains axillary validation methods.
    """

    content: Annotated[str, Field(max_length=2000)] | None = None
    """Message content."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

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

    @field_validator('embeds', mode='before')
    def convert_embeds_to_list(cls, embeds: Embed | list[Embed] | None) -> list[Embed] | None:
        """Convert single embed to a list.

        Args:
            embeds: Embeds to convert.

        Returns:
            Converted embeds.
        """
        if embeds is None:
            return embeds

        if not isinstance(embeds, Sequence):
            return [embeds]

        return embeds

    @field_validator('embeds')
    def extract_attachments_from_embeds_after(cls, embeds: list[Embed], info: ValidationInfo) -> list[Embed]:
        """Extract attachments from embeds.

        Args:
            embeds: Embeds to extract attachments from.
            info: Validation info.

        Returns:
            Extracted attachments.
        """
        if not embeds:
            return embeds

        attachments = []
        for embed in embeds:
            for embed_field_name in ('image', 'thumbnail'):
                attachment = getattr(embed, embed_field_name)
                if not attachment or isinstance(attachment, EmbedImage):
                    # If none or already an EmbedImage
                    continue

                if not isinstance(attachment, Attachment):
                    attachment = Attachment(
                        content=attachment,
                        filename=f'{embed_field_name}_{len(attachments)}',
                    )

                    mime_and_ext = get_content_type(attachment)
                    if mime_and_ext:
                        attachment.content_type = mime_and_ext[0]
                        attachment.filename = f'{attachment.filename}.{mime_and_ext[1]}'

                attachments.append(attachment)
                attachment_url = attachment.make_path()
                assert attachment_url  # noqa: S101

                setattr(embed, embed_field_name, EmbedImage(url=attachment_url))

        info.data[_EMBED_ATTACHMENT_DATA_FIELD] = attachments
        return embeds

    @field_validator('embeds')
    @classmethod
    def validate_embeds(cls, embeds: list[Embed] | None) -> list[Embed] | None:
        """Check total embed text length.

        Reference:
        https://discord.com/developers/docs/resources/message#message-object-message-structure

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
            total_embed_text_length += _embed_text_length(embed)

            if total_embed_text_length > MAX_EMBED_TEXT_LENGTH:
                raise ValueError(
                    'Total embed text length must be less than 6000 characters.',
                )

        return embeds

    @field_validator('components')
    @classmethod
    def validate_components(
        cls,
        components: Sequence[MessageComponentType] | MessageComponentType | None,
    ) -> Sequence[MessageComponentType] | None:
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

    @field_validator('attachments', mode='before')
    @classmethod
    def inject_embed_attachments(
        cls,
        attachments: ListAttachmentType | SingleAttachmentType | None | Any,  # noqa: ANN401
        info: ValidationInfo,
    ) -> list[Any] | None:
        """Inject embed attachments into the data.

        Args:
            attachments: Attachments to inject.
            info: Validation info.
        """
        embed_attachments: ListAttachmentType = info.data.get(_EMBED_ATTACHMENT_DATA_FIELD, [])
        if not attachments and not embed_attachments:
            return None

        match attachments:
            case None:
                attachments = [*embed_attachments]

            case Sequence():
                attachments = [*attachments, *embed_attachments]

            case _:
                attachments = [attachments, *embed_attachments]

        return attachments

    @field_validator('attachments', mode='before')
    @classmethod
    def convert_attachments(
        cls,
        attachments: list[Any] | None,
    ) -> list[Attachment] | None:
        """Convert files to attachments.

        Args:
            attachments: Attachments to convert.
            info: Validation info.

        Returns:
            Converted attachments.
        """
        if not attachments:
            return attachments

        converted_attachments = []
        for index, attachment in enumerate(attachments):
            if isinstance(attachment, AttachmentContentType):
                converted_attachments.append(Attachment(id=index, content=attachment))
            else:
                converted_attachments.append(attachment)

        return converted_attachments

    @field_validator('attachments')
    @classmethod
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
                # we do not want to modify the original attachment
                # it helps to use the same object in many requests
                # otherwise, this object can be conflicting with other because
                # it will have the id after the first request
                new_attachment_obj_with_id = attachment.model_copy(update={'id': index})
                attachments[index] = new_attachment_obj_with_id

        return attachments

    @model_validator(mode='after')
    def has_any_content(self) -> Self:
        """Validate message content.

        Reference:
        https://discord.com/developers/docs/resources/message#message-object-message-structure

        Args:
            values: Values to validate.

        Returns:
            Validated values.

        Raises:
            ValueError: If the message has no content or embeds.
        """
        # fmt: off
        has_any_content = bool(
            self.content
            or self.embeds
            or self.sticker_ids
            or self.components
            or self.attachments,
        )
        # fmt: on

        if not has_any_content:
            raise ValueError(
                'Message must have content, embeds, stickers, components or files',
            )

        return self

    @field_serializer('attachments', mode='wrap', when_used='json-unless-none')
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


def _embed_text_length(embed: Embed) -> int:
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
