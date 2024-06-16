import mimetypes
from pathlib import Path

from asyncord.client.stickers.models.requests import (
    CreateGuildStickerRequest,
    StickerFile,
    UpdateGuildStickerRequest,
)
from asyncord.client.stickers.resources import StickersResource
from tests.conftest import IntegrationTestData

TEST_STICKER = 'test_sticker.png'


async def test_sticker_cycle(
    stickers_res: StickersResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test create, get, update, delete sticker."""
    created_sticker = await stickers_res.create_guild_sticker(
        integration_data.guild_id,
        CreateGuildStickerRequest(
            name='test_sticker',
            description='test_sticker_description',
            tags='test_sticker_tags',
            file=StickerFile(
                content=f'tests/data/{TEST_STICKER}',
                content_type=Path(TEST_STICKER).name,
                filename=mimetypes.guess_type(TEST_STICKER)[0],
            ),
        ),
    )
    assert created_sticker

    sticker = await stickers_res.get_guild_sticker(
        integration_data.guild_id,
        created_sticker.id,
    )

    assert sticker.id == created_sticker.id

    updated_sticker = await stickers_res.update_guild_sticker(
        integration_data.guild_id,
        created_sticker.id,
        UpdateGuildStickerRequest(
            name='test_sticker_updated',
            description='test_sticker_description_updated',
            tags='test_sticker_tags_updated',
        ),
    )

    assert updated_sticker.name != created_sticker.name

    await stickers_res.delete_guild_sticker(
        integration_data.guild_id,
        created_sticker.id,
    )
