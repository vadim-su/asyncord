"""Models for stickers resource responses."""

from pydantic import BaseModel

from asyncord.client.models.stickers import StickerPack


class StickerPackListResponse(BaseModel):
    """Response model for list of sticker packs.

    Reference:
    https://discord.com/developers/docs/resources/sticker#list-sticker-packs-response-structure
    """

    sticker_packs: list[StickerPack]
    """List of sticker packs."""
