from collections.abc import Sequence

import pytest

from asyncord.client.messages.models.requests.components import (
    ActionRow,
    SelectMenu,
    SelectMenuOption,
)
from asyncord.client.messages.models.requests.components.buttons import AnyButtonWithCustomId, PrimaryButton


def test_wrap_component_to_list_in_action_row() -> None:
    """Test that components are wrapped in an ActionRow."""
    request = ActionRow([
        PrimaryButton(
            custom_id='button_0',
            label='Button',
        ),
    ])

    assert isinstance(request.components, Sequence)
    assert len(request.components) == 1
    assert isinstance(request.components[0], AnyButtonWithCustomId)
    assert request.components[0].custom_id == 'button_0'


def test_components_cannot_be_empty() -> None:
    """Test that components cannot be empty."""
    with pytest.raises(ValueError, match='Value should have at least 1 item'):
        ActionRow([])


def test_action_row_can_have_max_5_components() -> None:
    """Test that an ActionRow can have a maximum of 5 components."""
    # fmt: on
    with pytest.raises(ValueError, match='Value should have at most 5 items'):
        # fmt: off
        ActionRow([
            PrimaryButton(
                custom_id=f'button_{i}',
                label=f'Button {i}',
            )
            for i in range(6)
        ])
        # fmt: on


def test_dont_create_message_with_button_and_select_menu() -> None:
    """Test that an ActionRow containing a select menu cannot also contain buttons."""
    exc_text = 'ActionRow containing a select menu cannot also contain buttons'
    with pytest.raises(ValueError, match=exc_text):
        ActionRow(
            components=[
                PrimaryButton(
                    custom_id='custom_id',
                    label='Button',
                ),
                SelectMenu(
                    custom_id='custom',
                    options=[
                        SelectMenuOption(label='Option 1', value='option_1'),
                    ],
                ),
            ],
        )
