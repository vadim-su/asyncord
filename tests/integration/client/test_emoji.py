from asyncord.client.emojis.resources import EmojiResource

from asyncord.client.emojis.models.requests import CreateEmojiRequest, UpdateEmojiRequest


from tests.conftest import IntegrationTestData

TEST_EMOJI = {'name': 'test_emoji', 'path': 'test_emoji.png'}


async def test_crete_get_modify_delete_guild_emoji(
    emoji_res: EmojiResource,
) -> None:
    """Test create, get and delete guild emoji."""
    with open(f'tests/data/{TEST_EMOJI['path']}', 'rb') as f:
        emoji_data = f.read()

    emoji = await emoji_res.create_guild_emoji(
        CreateEmojiRequest(
            name=TEST_EMOJI['name'],
            image=emoji_data,
        ),
    )
    assert emoji.name == TEST_EMOJI['name']

    emoji_from_server = await emoji_res.get_guild_emoji(emoji.id)

    assert emoji_from_server.name == TEST_EMOJI['name']

    updated_emoji = await emoji_res.update_guild_emoji(
        emoji.id,
        UpdateEmojiRequest(
            name=f'{TEST_EMOJI['name']}_updated',
        ),
    )
    assert TEST_EMOJI['name'] != updated_emoji.name

    await emoji_res.delete_guild_emoji(emoji.id)

if __name__ == '__main__':
    with open(f'tests/data/{TEST_EMOJI['path']}', 'rb') as f:
        emoji_data = f.read()
    print(emoji_data)