from collections.abc import AsyncGenerator, Callable, Iterable
from pathlib import Path

import pytest

from asyncord.client.models.stickers import Sticker
from asyncord.client.stickers.models.requests import (
    CreateGuildStickerRequest,
    UpdateGuildStickerRequest,
)
from asyncord.client.stickers.resources import StickersResource
from tests.conftest import IntegrationTestData

TEST_STICKER = Path('tests/data/test_sticker.png')


@pytest.fixture
async def sticker(
    stickers_res: StickersResource,
    integration_data: IntegrationTestData,
) -> AsyncGenerator[Sticker, None]:
    """Create a sticker and delete it after the test."""
    sticker = await stickers_res.create_guild_sticker(
        integration_data.guild_id,
        CreateGuildStickerRequest(
            name='TestSticker',
            description='Test sticker description',
            tags='test sticker tags',
            image_data=TEST_STICKER,
        ),
    )
    yield sticker
    await stickers_res.delete_guild_sticker(
        integration_data.guild_id,
        sticker.id,
    )


async def test_get_sticker(sticker: Sticker, stickers_res: StickersResource) -> None:
    """Test getting a sticker."""
    assert await stickers_res.get_sticker(sticker.id)


async def test_get_sticker_pack_list(stickers_res: StickersResource) -> None:
    """Test getting a list of sticker packs."""
    assert await stickers_res.get_sticker_pack_list()


async def test_get_guild_stickers_list(
    stickers_res: StickersResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting a list of stickers in a guild."""
    stickers = await stickers_res.get_guild_stickers_list(integration_data.guild_id)
    assert isinstance(stickers, list)


async def test_get_guild_sticker(
    sticker: Sticker,
    stickers_res: StickersResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting a sticker in a guild."""
    guild_sticker = await stickers_res.get_guild_sticker(
        integration_data.guild_id,
        sticker.id,
    )
    assert guild_sticker.id == sticker.id


async def test_update_guild_sticker(
    sticker: Sticker,
    stickers_res: StickersResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test updating a sticker in a guild."""
    updated_sticker = await stickers_res.update_guild_sticker(
        integration_data.guild_id,
        sticker.id,
        UpdateGuildStickerRequest(
            name='UpdatedSticker',
            description='Updated sticker description',
            tags='updated sticker tags',
        ),
    )
    assert updated_sticker.name == 'UpdatedSticker'
    assert updated_sticker.description == 'Updated sticker description'
    assert updated_sticker.tags == 'updated sticker tags'


@pytest.mark.parametrize(
    'iterable_type',
    [
        set,
        list,
        tuple,
        iter,
    ],
)
def test_tags_can_be_iterable(iterable_type: Callable[[Iterable[str]], None]) -> None:
    """Test tags can be an iterable."""
    tags = iterable_type(['updated', 'sticker', 'tags'])
    model = UpdateGuildStickerRequest(tags=tags)
    assert model.tags == {'updated', 'sticker', 'tags'}


@pytest.mark.parametrize(
    'tags',
    [
        'updated, sticker, tags',
        'updated  , sticker, tags',
        '  updated,   sticker , \ntags   ',
    ],
)
def test_tags_can_be_str(tags: str) -> None:
    """Test tags can be a string with comma-separated values."""
    model = UpdateGuildStickerRequest(
        tags=tags,
    )
    assert model.tags == {'updated', 'sticker', 'tags'}


def test_tags_too_long() -> None:
    """Test tags cannot be too long."""
    with pytest.raises(ValueError, match='length must be less than'):
        UpdateGuildStickerRequest(tags='a' * 201)
