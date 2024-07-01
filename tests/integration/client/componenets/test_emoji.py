import pytest

from asyncord.client.messages.models.requests.components import ComponentEmoji


def test_emoji_fail_with_both_name_and_id() -> None:
    """Test that an emoji can contain a name or an id."""
    with pytest.raises(ValueError, match='Only one of'):
        ComponentEmoji(name='emoji_name', id=1241)


def test_emoji_fail_with_no_name_and_id() -> None:
    """Test that an emoji must contain a name or an id."""
    with pytest.raises(ValueError, match='least one of'):
        ComponentEmoji()
