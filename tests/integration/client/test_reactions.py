import pytest

from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.messages.resources import MessageResource
from asyncord.client.reactions.resources import ReactionResource
from tests.conftest import IntegrationTestData

TEST_EMOJI1 = '👍'
TEST_EMOJI2 = '👎'


@pytest.fixture
async def reactions_res(
    message: MessageResponse,
    messages_res: MessageResource,
) -> ReactionResource:
    """Get reactions resource for the message."""
    resource = messages_res.reactions(message.id)
    await resource.add(TEST_EMOJI1)
    await resource.add(TEST_EMOJI2)
    return resource


async def test_get_reactions(
    reactions_res: ReactionResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test adding and getting reactions."""
    assert (await reactions_res.get(TEST_EMOJI1))[0].id == integration_data.member_id


async def test_get_reactions_with_after_param(
    reactions_res: ReactionResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test adding and getting reactions with the after parameter."""
    reactions = await reactions_res.get(TEST_EMOJI1, after=integration_data.member_id)
    # it should return an empty list because there are no reactions after the bot test member
    assert not reactions


async def test_get_reactions_with_limit_param(
    reactions_res: ReactionResource,
) -> None:
    """Test adding and getting reactions with the limit parameter.

    Dummy test to check if the limit parameter is sending in general.
    """
    reactions = await reactions_res.get(TEST_EMOJI1, limit=1)
    assert len(reactions) == 1


@pytest.mark.parametrize('user_id', [None, 'member_id', '@me'])
async def test_delete_reaction(
    user_id: str | None,
    reactions_res: ReactionResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test deleting own reaction."""
    if user_id == 'member_id':
        user_id = integration_data.member_id

    await reactions_res.delete(TEST_EMOJI1, user_id=user_id)

    assert not await reactions_res.get(TEST_EMOJI1)


async def test_delete_all_reactions(reactions_res: ReactionResource) -> None:
    """Test deleting all reactions."""
    await reactions_res.delete()
    assert not await reactions_res.get(TEST_EMOJI1)
    assert not await reactions_res.get(TEST_EMOJI2)


async def test_delete_all_reactions_for_emoji(reactions_res: ReactionResource) -> None:
    """Test deleting all reactions for an emoji."""
    await reactions_res.delete(TEST_EMOJI1)
    assert not await reactions_res.get(TEST_EMOJI1)
    assert await reactions_res.get(TEST_EMOJI2)


async def test_delete_fail_on_user_id_without_emoji(reactions_res: ReactionResource) -> None:
    """Test deleting a reaction with a user id but no emoji."""
    with pytest.raises(ValueError, match='Cannot delete a reaction for a user without an emoji.'):
        await reactions_res.delete(user_id='123')
