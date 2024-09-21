from collections.abc import AsyncGenerator
from pathlib import Path

import pytest

from asyncord.client.emojis.models.requests import CreateEmojiRequest, UpdateEmojiRequest
from asyncord.client.emojis.models.responses import EmojiResponse
from asyncord.client.emojis.resources import EmojiResource

EMOJI_PATH = Path('tests/data/test_emoji.png')


@pytest.fixture
async def emoji(emoji_res: EmojiResource) -> AsyncGenerator[EmojiResponse, None]:
    """Fixture to create a guild emojim and remove it after the test."""
    emoji = await emoji_res.create_guild_emoji(
        CreateEmojiRequest(
            name='test_emoji',
            image=EMOJI_PATH,
        ),
    )
    yield emoji
    await emoji_res.delete_guild_emoji(emoji.id)  # type: ignore (id should be set after creation)


async def test_get_guild_emoji(
    emoji: EmojiResponse,
    emoji_res: EmojiResource,
) -> None:
    """Test getting a guild emoji."""
    emoji = await emoji_res.get_guild_emoji(emoji.id)  # type: ignore
    assert emoji.id == emoji.id
    assert emoji.name == emoji.name


async def test_get_guild_emojis(
    emoji: EmojiResponse,
    emoji_res: EmojiResource,
) -> None:
    """Test getting all guild emojis."""
    emojis = await emoji_res.get_guild_emojis()
    assert emoji.id in [emoji.id for emoji in emojis]


async def test_update_guild_emoji(
    emoji: EmojiResponse,
    emoji_res: EmojiResource,
) -> None:
    """Test updating a guild emoji."""
    updated_emoji = await emoji_res.update_guild_emoji(
        emoji.id,  # type: ignore
        UpdateEmojiRequest(
            name='updated_emoji',
        ),
    )
    assert updated_emoji.name == 'updated_emoji'
