"""Represents a sticker that can be sent in messages."""

from __future__ import annotations

import enum

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel

from asyncord.client.users.models.responses import UserResponse
from asyncord.snowflake import Snowflake

__all__ = (
    'Sticker',
    'StickerFormatType',
    'StickerPack',
    'StickerType',
)


@enum.unique
class StickerType(enum.IntEnum):
    """Represents the type of a sticker.

    Reference:
    https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-types
    """

    STANDARD = 1
    """Official sticker in a pack, part of Nitro or in a removed purchasable pack."""

    GUILD = 2
    """Sticker uploaded to a guild for the guild's members."""


@enum.unique
class StickerFormatType(enum.IntEnum):
    """Represents the format type of a sticker.

    Reference:
    https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-format-types
    """

    PNG = 1
    """PNG sticker format."""

    APNG = 2
    """APNG sticker format."""

    LOTTIE = 3
    """LOTTIE sticker format."""

    GIF = 4
    """GIF sticker format."""


class Sticker(BaseModel):
    """Represents a sticker that can be sent in messages.

    Reference:
    https://discord.com/developers/docs/resources/sticker#sticker-object
    """

    id: Snowflake
    """ID of the sticker."""

    pack_id: Snowflake | None = None
    """ID of the pack the sticker is from.

    Only for standard stickers.
    """

    name: str
    """Name of the sticker."""

    description: str | None
    """Description of the sticker."""

    tags: str
    """Autocomplete/suggestion tags for the sticker (max 200 characters).

    A comma separated list of keywords is the format used in this field
    by standard stickers, but this is just a convention. Incidentally the client
    will always use a name generated from an emoji as the value of this field
    when creating or modifying a guild sticker.
    """

    asset: str | None = None
    """Deprecated previously the sticker asset hash, now an empty string."""

    type: FallbackAdapter[StickerType]
    """Type of sticker."""

    format_type: FallbackAdapter[StickerFormatType]
    """Type of sticker format."""

    available: bool | None = None
    """Whether this guild sticker can be used, may be false due to loss of Server Boosts."""

    guild_id: Snowflake | None = None
    """ID of the guild that owns this sticker."""

    user: UserResponse | None = None
    """User that uploaded the guild sticker."""

    sort_value: int | None = None
    """Standard sticker's sort order within its pack."""


class StickerPack(BaseModel):
    """Represents a sticker pack.

    Reference:
    https://discord.com/developers/docs/resources/sticker#sticker-pack-object
    """

    id: Snowflake
    """ID of the pack."""

    stickers: list[Sticker]
    """Stickers in the pack."""

    name: str
    """Name of the pack."""

    sku_id: Snowflake
    """ID of a sticker in the pack which is shown as the pack's icon."""

    cover_sticker_id: Snowflake | None = None
    """ID of a sticker in the pack which is shown as the pack's thumbnail."""

    description: str
    """Description of the pack."""

    banner_asset_id: Snowflake | None = None
    """ID of the sticker asset for the pack's banner image."""
