"""Models for guild template requests."""

from typing import Annotated

from pydantic import BaseModel, Field

from asyncord.base64_image import Base64ImageInputType

__all__ = (
    'CreateGuildFromTemplateRequest',
    'CreateGuildTemplateRequest',
    'UpdateGuildTemplateRequest',
)


class CreateGuildFromTemplateRequest(BaseModel):
    """Create guild from template request.

    Reference:
    https://discord.com/developers/docs/resources/guild-template#create-guild-from-guild-template-json-params
    """

    name: str | None = Field(min_length=2, max_length=100)
    """Name of the guild (2-100 characters)."""

    icon: Base64ImageInputType | None = None
    """Base64 encoded 128x128 image for the guild icon."""


class CreateGuildTemplateRequest(BaseModel):
    """Create guild template request.

    Reference:
    https://discord.com/developers/docs/resources/guild-template#create-guild-template-json-params
    """

    name: str = Field(min_length=1, max_length=100)
    """Name of the template (1-100 characters)."""

    description: Annotated[str, Field(max_length=120)] | None = None
    """Description for the template (0-120 characters)."""


class UpdateGuildTemplateRequest(BaseModel):
    """Update guild template request.

    Reference:
    https://discord.com/developers/docs/resources/guild-template#modify-guild-template-json-params
    """

    name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    """Name of the template (1-100 characters)."""

    description: Annotated[str, Field(max_length=120)] | None = None
    """Description for the template (0-120 characters)."""
