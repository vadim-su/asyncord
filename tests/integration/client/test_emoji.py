from asyncord.client.emojis.resources import EmojiResource

from asyncord.client.emojis.models.requests import CreateEmojiRequest, UpdateEmojiRequest


from tests.conftest import IntegrationTestData

TEST_EMOJI = {
    'name': 'test_emoji',
    'path': 'test_emoji.png',
}


async def test_guild_emoji_lifecycle(
    emoji_res: EmojiResource,
) -> None:
    """Test the lifecycle (create, get, modify, delete) of a guild emoji."""
    with open(f'tests/data/{TEST_EMOJI['path']}', 'rb') as f:
        emoji_data = f.read()

    # Check initial state
    initial_emojis = await emoji_res.get_guild_emojis()
    assert TEST_EMOJI['name'] not in [emoji.name for emoji in initial_emojis]

    # Create the emoji
    emoji = await emoji_res.create_guild_emoji(
        CreateEmojiRequest(
            name=TEST_EMOJI['name'],
            image=emoji_data,
        ),
    )
    assert emoji.name == TEST_EMOJI['name']

    # Check that the emoji exists in the guild
    emojis_after_creation = await emoji_res.get_guild_emojis()
    assert TEST_EMOJI['name'] in [emoji.name for emoji in emojis_after_creation]

    # Modify the emoji
    updated_emoji = await emoji_res.update_guild_emoji(
        emoji.id,
        UpdateEmojiRequest(
            name=f'{TEST_EMOJI['name']}_updated',
        ),
    )
    assert TEST_EMOJI['name'] != updated_emoji.name

    # Check that the updated emoji exists in the guild
    emojis_after_modification = await emoji_res.get_guild_emojis()
    assert f'{TEST_EMOJI['name']}_updated' in [emoji.name for emoji in emojis_after_modification]

    # Delete the emoji
    await emoji_res.delete_guild_emoji(emoji.id)

    # Check that the emoji no longer exists in the guild
    emojis_after_deletion = await emoji_res.get_guild_emojis()
    assert f'{TEST_EMOJI['name']}_updated' not in [emoji.name for emoji in emojis_after_deletion]
