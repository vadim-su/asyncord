"""Models for stickers resource requests."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    SerializerFunctionWrapHandler,
    WrapSerializer,
)

from asyncord.client.models.attachments import AttachmentContentType

__all__ = (
    'CreateGuildStickerRequest',
    'TagsType',
    'UpdateGuildStickerRequest',
)

MAX_TAG_SIZE = 200
"""Maximum length of tags in sticker requests after serialization."""


class CreateGuildStickerRequest(BaseModel, arbitrary_types_allowed=True):
    """Request model for creating a guild sticker.

    Reference:
    https://discord.com/developers/docs/resources/sticker#create-guild-sticker-form-params
    """

    name: str = Field(min_length=2, max_length=30)
    """Name of sticker."""

    description: str = Field(min_length=2, max_length=100)
    """Description of sticker."""

    tags: TagsType
    """Autocomplete/suggestion tags for the sticker."""

    image_data: AttachmentContentType = Field(serialization_alias='file')
    """Sticker image data.

    It can be raw data, a file-like object, or a path to a file. Can't be a string or a URL.
    Supported file types: PNG, APNG, WEBP, LOTTIE.
    """


class UpdateGuildStickerRequest(BaseModel):
    """Request model for updating a guild sticker.

    Reference:
    https://discord.com/developers/docs/resources/sticker#modify-guild-sticker-json-params
    """

    name: Annotated[str, Field(min_length=2, max_length=30)] | None = None
    """Name of sticker."""

    description: Annotated[str, Field(min_length=2, max_length=100)] | None = None
    """Description of sticker."""

    tags: TagsType | None = None
    """Autocomplete/suggestion tags for the sticker."""


def _validate_tags(tags: Sequence[str] | set[str] | str) -> set[str]:
    """Validate tags length.

    On serialization, tags converted to a string with a comma and space separator.
    So, the total length of a resulting string must be less than or equal to 200.

    The validator converts tags to a set if it's a string.
    """
    if isinstance(tags, str):
        tags = set(tag.strip() for tag in tags.split(','))
    else:
        tags = set(tag for tag in tags)

    total_tags_length = (
        sum(len(tag) for tag in tags)  # total length of all tags
        + (len(tags) - 1) * 2  # length of all commas and spaces between tags
    )

    if total_tags_length > MAX_TAG_SIZE:
        err = ValueError('Tags length must be less than or equal to 200')
        err.add_note('Do not forget that each tag is separated by a comma with a space on serializing')
        raise err

    return tags


def _serialize_tags_to_string(
    tags: set[str],
    next_serializer: SerializerFunctionWrapHandler,
) -> str:
    """Serialize tags to a string with a comma and space separator."""
    return next_serializer(', '.join(tags))


type TagsType = Annotated[
    Sequence[str] | set[str] | str,
    BeforeValidator(_validate_tags),
    WrapSerializer(_serialize_tags_to_string),
    set[str],
]
"""Type for tags field in sticker requests.

Tags are serialized to a string with a comma and space separator and result string length
must be less than or equal to 200.
"""


# Models should rebuild after defining TagsType
CreateGuildStickerRequest.model_rebuild()
UpdateGuildStickerRequest.model_rebuild()
