import datetime

from pydantic import BaseModel, Field

from asyncord.client.messages.models.common import EmbedType
from asyncord.color import ColorInput


class EmbedFooterInput(BaseModel):
    """Object representing footer of an embed.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-footer-structure
    """

    text: str = Field(max_length=2048)
    """Text of the footer."""

    icon_url: str | None = None
    """URL of the footer icon (only supports http(s) and attachments)."""

    proxy_icon_url: str | None = None
    """Proxied URL of the footer icon."""


class EmbedImageInput(BaseModel):
    """Object representing image in an embed.

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


class EmbedThumbnailInput(BaseModel):
    """Object representing thumbnail in an embed.

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


class EmbedVideoInput(BaseModel):
    """Object representing video in an embed.

    Bots can not send this object.
    Discord API will ignore it if provided.

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


class EmbedProviderInput(BaseModel):
    """Object representing the provider of an embed.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-provider-structure
    """

    name: str | None = None
    """Name of the provider."""

    url: str | None = None
    """URL of the provider."""


class EmbedAuthorInput(BaseModel):
    """Object representing the author of an embed.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-author-structure
    """

    name: str = Field(max_length=256)
    """Name of author."""

    url: str | None = None
    """URL of author."""

    icon_url: str | None = None
    """URL of author icon (only supports http(s) and attachments)."""

    proxy_icon_url: str | None = None
    """Proxied URL of author icon."""


class EmbedFieldInput(BaseModel):
    """Embed field object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object-embed-field-structure
    """

    name: str = Field(max_length=256)
    """Name of the field."""

    value: str = Field(max_length=1024)
    """Value of the field."""

    inline: bool | None = None
    """Whether or not this field should display inline."""


class EmbedInput(BaseModel):
    """Embed object.

    Reference:
    https://discord.com/developers/docs/resources/channel#embed-object
    """

    title: str | None = Field(None, max_length=256)
    """Title of the embed."""

    type: EmbedType | None = None
    """Type of the embed.

    Always "rich" for webhook embeds.
    """

    description: str | None = Field(None, max_length=4096)
    """Description of the embed."""

    url: str | None = None
    """URL of the embed."""

    timestamp: datetime.datetime | None = None
    """Timestamp of the embed content."""

    color: ColorInput | None = None
    """Color code of the embed."""

    footer: EmbedFooterInput | None = None
    """Footer information."""

    image: EmbedImageInput | None = None
    """Image information."""

    thumbnail: EmbedThumbnailInput | None = None
    """Thumbnail information."""

    video: EmbedVideoInput | None = None
    """Video information.
    
    Bots can not use this field.
    Discord API will ignore it if provided.
    """

    provider: EmbedProviderInput | None = None
    """Provider information."""

    author: EmbedAuthorInput | None = None
    """Author information."""

    fields: list[EmbedFieldInput] = Field(default_factory=list, max_length=25)
    """List of fields.

    Maximum of 25 items.
    """
