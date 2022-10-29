from __future__ import annotations

import enum

from pydantic import BaseModel

from asyncord.snowflake import Snowflake
from asyncord.client.models.users import User


class Sticker(BaseModel):
    """Represents a sticker that can be sent in messages.

    https://discord.com/developers/docs/resources/sticker#sticker-object
    """

    id: Snowflake
    """The ID of the sticker"""

    pack_id: Snowflake | None = None
    """for standard stickers, id of the pack the sticker is from"""

    name: str
    """name of the sticker"""

    description: str | None
    """description of the sticker"""

    tags: str
    """autocomplete/suggestion tags for the sticker (max 200 characters)

    A comma separated list of keywords is the format used in this field
    by standard stickers, but this is just a convention. Incidentally the client
    will always use a name generated from an emoji as the value of this field
    when creating or modifying a guild sticker.
    """

    asset: str | None = None
    """Deprecated previously the sticker asset hash, now an empty string"""

    type: StickerType
    """type of sticker"""

    format_type: StickerFormatType
    """type of sticker format"""

    available: bool | None = None
    """whether this guild sticker can be used, may be false due to loss of Server Boosts"""

    guild_id: Snowflake | None = None
    """id of the guild that owns this sticker"""

    user: User | None = None
    """the user that uploaded the guild sticker"""

    sort_value: int | None = None
    """the standard sticker's sort order within its pack"""


class StickerPack(BaseModel):
    """Represents a sticker pack.

    https://discord.com/developers/docs/resources/sticker#sticker-pack-object
    """

    id: Snowflake
    """ID of the pack"""

    stickers: list[Sticker]
    """Stickers in the pack"""

    name: str
    """Name of the pack"""

    sku_id: Snowflake
    """ID of a sticker in the pack which is shown as the pack's icon"""

    cover_sticker_id: Snowflake | None = None
    """ID of a sticker in the pack which is shown as the pack's thumbnail"""

    description: str
    """Description of the pack"""

    banner_asset_id: Snowflake | None = None
    """ID of the sticker asset for the pack's banner image"""


@enum.unique
class StickerType(enum.IntEnum):
    """https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-types"""

    STANDARD = 1
    """an official sticker in a pack, part of Nitro or in a removed purchasable pack"""

    GUILD = 2
    """a sticker uploaded to a guild for the guild's members"""


@enum.unique
class StickerFormatType(enum.IntEnum):
    """https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-format-types"""

    PNG = 1
    """PNG sticker format"""

    APNG = 2
    """APNG sticker format"""

    LOTTIE = 3
    """LOTTIE sticker format"""


Sticker.update_forward_refs()
