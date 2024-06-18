from pathlib import Path

from asyncord.client.stickers.models.requests import (
    CreateGuildStickerRequest,
    UpdateGuildStickerRequest,
)
from asyncord.client.stickers.resources import StickersResource
from tests.conftest import IntegrationTestData

TEST_STICKER = Path('tests/data/test_sticker.png')


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
            image_data=TEST_STICKER,
        ),
    )
    try:
        sticker = await stickers_res.get_guild_sticker(
            integration_data.guild_id,
            created_sticker.id,
        )

        assert sticker.id == created_sticker.id
        assert sticker.name == 'test_sticker'

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

    finally:
        await stickers_res.delete_guild_sticker(
            integration_data.guild_id,
            created_sticker.id,
        )
