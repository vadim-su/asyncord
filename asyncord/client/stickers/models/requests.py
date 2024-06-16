"""Models for stickers resource requests."""

from __future__ import annotations

from io import BufferedReader, IOBase
from pathlib import Path
from typing import Annotated, Any, cast

from pydantic import BaseModel, Field, ValidationError

from asyncord.client.http.client import make_payload_form
from asyncord.client.http.models import FormField, FormPayload

type StickerContentType = bytes | bytearray | memoryview | BufferedReader | IOBase | Path
"""Sticker content type.

It can be raw data, a file-like object, or a path to a file.
"""


class StickerFile(BaseModel, arbitrary_types_allowed=True):
    """Stick file object used for creating stickers."""

    content: Annotated[StickerContentType | None, Field(exclude=True)]
    """Sticker file content."""

    content_type: str | None = None

    """Sticker file content type."""

    filename: str | None = None
    """Sticker file name."""


class CreateGuildStickerRequest(BaseModel):
    """Request model for creating a guild sticker.

    Reference:
    https://canary.discord.com/developers/docs/resources/sticker#create-guild-sticker-form-params
    """

    name: str = Field(None, min_length=2, max_length=30)
    """Name of sticker."""

    description: str = Field(None, min_length=2, max_length=100)
    """Description of sticker."""

    tags: str = Field(None, max_length=200)
    """Autocomplete/suggestion tags for the sticker (max 200 characters)."""

    file: StickerFile = Field(None, exclude=True)
    """Sticker content.

    This field is not part of the Discord API and will not be serialized.
    """


class UpdateGuildStickerRequest(BaseModel):
    """Request model for updating a guild sticker.

    Reference:
    https://canary.discord.com/developers/docs/resources/sticker#modify-guild-sticker-json-params
    """

    name: str | None = Field(None, min_length=2, max_length=30)
    """Name of sticker."""

    description: str | None = Field(None, min_length=2, max_length=100)
    """Description of sticker."""

    tags: str | None = Field(None, max_length=200)
    """Autocomplete/suggestion tags for the sticker (max 200 characters)."""


def make_sticker_payload(
    sticker_data: CreateGuildStickerRequest,
) -> FormPayload | dict[str, Any]:
    """Convert upload sticker model to a payload.

    Args:
        sticker_data: Sticker upload request model with sticker.
    """
    payload_model_data = sticker_data
    json_payload = payload_model_data.model_dump(mode='json', exclude_unset=True)
    if not sticker_data.file:  # type: ignore
        raise ValidationError('Sticker content is required.')

    sticker = cast(StickerFile, sticker_data.file)  # type: ignore

    file_form_fields = {
        'file': FormField(
            value=sticker.content,
            content_type=sticker.content_type,
            filename=sticker.filename,
        ),
    }
    return make_payload_form(json_payload=json_payload, **file_form_fields)
