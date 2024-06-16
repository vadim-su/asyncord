"""Models for embeds in message responses."""

import datetime

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel, Field

from asyncord.client.messages.models.common import EmbedType
from asyncord.color import Color

__all__ = (
    'EmbedAuthorOut',
    'EmbedFieldOut',
    'EmbedFooterOut',
    'EmbedImageOut',
    'EmbedOut',
    'EmbedProviderOut',
    'EmbedThumbnailOut',
    'EmbedVideoOut',
)


class EmbedFooterOut(BaseModel):
    """Embed footer object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-footer-structure
    """

    text: str
    """Text of the footer."""

    icon_url: str | None = None
    """URL of the footer icon (only supports http(s) and attachments)."""

    proxy_icon_url: str | None = None
    """Proxied URL of the footer icon."""


class EmbedImageOut(BaseModel):
    """Embed image object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-image-structure
    """

    url: str
    """Source URL of image (only supports http(s) and attachments)."""

    proxy_url: str | None = None
    """Proxied URL of image."""

    height: int | None = None
    """Height of image."""

    width: int | None = None
    """Width of image."""


class EmbedThumbnailOut(BaseModel):
    """Embed thumbnail object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-thumbnail-structure
    """

    url: str
    """Source URL of thumbnail (only supports http(s) and attachments)."""

    proxy_url: str | None = None
    """Proxied URL of thumbnail."""

    height: int | None = None
    """Height of thumbnail."""

    width: int | None = None
    """Width of thumbnail."""


class EmbedVideoOut(BaseModel):
    """Embed video object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-video-structure
    """

    url: str | None = None
    """Source URL of the video."""

    proxy_url: str | None = None
    """Proxied URL of the video."""

    height: int | None = None
    """Height of the video."""

    width: int | None = None
    """Width of the video."""


class EmbedProviderOut(BaseModel):
    """Embed provider object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-provider-structure
    """

    name: str | None = None
    """Name of the provider."""

    url: str | None = None
    """URL of the provider."""


class EmbedAuthorOut(BaseModel):
    """Embed author object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-author-structure
    """

    name: str
    """Name of author."""

    url: str | None = None
    """URL of author."""

    icon_url: str | None = None
    """URL of author icon (only supports http(s) and attachments)."""

    proxy_icon_url: str | None = None
    """Proxied URL of author icon."""


class EmbedFieldOut(BaseModel):
    """Embed field object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-field-structure
    """

    name: str
    """Name of the field."""

    value: str
    """Value of the field."""

    inline: bool | None = None
    """Whether or not this field should display inline."""


class EmbedOut(BaseModel):
    """Embed object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object
    """

    title: str | None = None
    """Title of the embed."""

    type: FallbackAdapter[EmbedType] | None = None
    """Type of the embed.

    Always "rich" for webhook embeds.
    """

    description: str | None = None
    """Description of the embed."""

    url: str | None = None
    """URL of the embed."""

    timestamp: datetime.datetime | None = None
    """Timestamp of the embed content."""

    color: Color | None = None
    """Color code of the embed."""

    footer: EmbedFooterOut | None = None
    """Footer information."""

    image: EmbedImageOut | None = None
    """Image information."""

    thumbnail: EmbedThumbnailOut | None = None
    """Thumbnail information."""

    video: EmbedVideoOut | None = None
    """Video information.

    Bots can not use this field.
    Discord API will ignore it if provided.
    """

    provider: EmbedProviderOut | None = None
    """Provider information."""

    author: EmbedAuthorOut | None = None
    """Author information."""

    fields: list[EmbedFieldOut] = Field(default_factory=list)
    """List of fields.

    Maximum of 25 items.
    """
