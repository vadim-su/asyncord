"""Request models for guilds."""

from pydantic import BaseModel

from asyncord.base64_image import Base64ImageInputType

__all__ = (
    'CreateEmojiRequest',
    'UpdateEmojiRequest',
)


class CreateEmojiRequest(BaseModel):
    """Create emoji request model.

    Reference:
    https://discord.com/developers/docs/resources/emoji#create-guild-emoji-json-params
    """

    name: str
    """Emoji name."""

    image: Base64ImageInputType
    """Emoji image."""

    roles: list[int] | None = None


class UpdateEmojiRequest(BaseModel):
    """Update emoji request model.

    Reference:
    https://discord.com/developers/docs/resources/emoji#modify-guild-emoji-json-params
    """

    name: str | None = None
    """New emoji name."""

    roles: list[int] | None = None
    """New roles for the emoji."""
