from asyncord.client.reactions.resources import ReactionResource
from tests.conftest import IntegrationTestData


async def test_add_and_get_reactions(
    reactions_res: ReactionResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test adding and getting reactions."""
    test_emoji1 = '👍'
    test_emoji2 = '👎'

    await reactions_res.add(test_emoji1)
    await reactions_res.add(test_emoji2)

    assert (await reactions_res.get(test_emoji1))[0].id == integration_data.member_id
    assert (await reactions_res.get(test_emoji2))[0].id == integration_data.member_id


async def test_delete_own_reaction(reactions_res: ReactionResource) -> None:
    """Test deleting own reaction."""
    test_emoji = '👍'
    await reactions_res.add(test_emoji)
    assert await reactions_res.get(test_emoji)

    await reactions_res.delete_own_reaction(test_emoji)
    assert not await reactions_res.get(test_emoji)


async def test_delete_user_reaction(reactions_res: ReactionResource, integration_data: IntegrationTestData) -> None:
    """Test deleting user reaction."""
    test_emoji = '👍'
    await reactions_res.add(test_emoji)
    assert await reactions_res.get(test_emoji)

    await reactions_res.delete(test_emoji, integration_data.member_id)
    assert not await reactions_res.get(test_emoji)


async def test_delete_all_reactions(reactions_res: ReactionResource) -> None:
    """Test deleting all reactions."""
    test_emoji1 = '👍'
    test_emoji2 = '👎'

    await reactions_res.add(test_emoji1)
    await reactions_res.add(test_emoji2)
    assert await reactions_res.get(test_emoji1)
    assert await reactions_res.get(test_emoji2)

    await reactions_res.delete()
    assert not await reactions_res.get(test_emoji1)
    assert not await reactions_res.get(test_emoji2)


async def test_delete_all_reactions_for_emoji(reactions_res: ReactionResource) -> None:
    """Test deleting all reactions for an emoji."""
    test_emoji1 = '👍'
    test_emoji2 = '👎'

    await reactions_res.add(test_emoji1)
    await reactions_res.add(test_emoji2)
    assert await reactions_res.get(test_emoji1)
    assert await reactions_res.get(test_emoji2)

    await reactions_res.delete(test_emoji1)
    assert not await reactions_res.get(test_emoji1)
    assert await reactions_res.get(test_emoji2)


async def test_add_and_delete(
    reactions_res: ReactionResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test adding and deleting reactions."""
    await reactions_res.add(integration_data.custom_emoji)
    assert await reactions_res.get(integration_data.custom_emoji)

    await reactions_res.delete(integration_data.custom_emoji)
    assert not await reactions_res.get(integration_data.custom_emoji)
