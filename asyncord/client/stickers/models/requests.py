"""Models for stickers resource requests."""

from pydantic import BaseModel, Field

from asyncord.client.messages.models.requests.messages import AttachedFile


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

    file: AttachedFile = Field(default_factory=None, exclude=True)
    """Sticker file to upload.

    Must be a PNG, APNG, GIF, Lottie JSON file.
    Max 512 KiB.
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
