from typing import Protocol

import pytest

from asyncord.client.interactions.models.requests import InteractionCreateMessageData, InteractionUpdateMessageData
from asyncord.client.messages.models.requests.components import (
    ActionRow,
    Button,
    ButtonStyle,
    Component,
    SelectMenu,
    SelectMenuOption,
)
from asyncord.client.messages.models.requests.messages import CreateMessageRequest, UpdateMessageRequest
from asyncord.client.messages.resources import MessageResource
from asyncord.client.threads.models.requests import ThreadMessage


async def test_create_message_with_buttons(messages_res: MessageResource) -> None:
    """Test creating a message with buttons."""
    components: list[Component] = [
        ActionRow(
            components=[
                Button(
                    label='Primary',
                    style=ButtonStyle.PRIMARY,
                    custom_id='primary',
                ),
                Button(
                    label='Secondary',
                    style=ButtonStyle.SECONDARY,
                    custom_id='secondary',
                ),
                Button(
                    label='Success',
                    style=ButtonStyle.SUCCESS,
                    custom_id='success',
                ),
                Button(
                    label='Danger',
                    style=ButtonStyle.DANGER,
                    custom_id='danger',
                ),
                Button(
                    label='Link',
                    style=ButtonStyle.LINK,
                    url='https://discord.com',
                ),  # type: ignore
            ],
        ),
    ]
    message = await messages_res.create(
        CreateMessageRequest(
            content='Test message with buttons',
            components=components,
        ),
    )

    try:
        assert message.content == 'Test message with buttons'
        assert len(message.components) == len(components)
    finally:
        await messages_res.delete(message.id)


def test_dont_create_message_with_button_and_select_menu() -> None:
    """Test that an ActionRow containing a select menu cannot also contain buttons."""
    exc_text = 'ActionRow containing a select menu cannot also contain buttons'
    with pytest.raises(ValueError, match=exc_text):
        ActionRow(
            components=[
                Button(custom_id='custom_id'),
                SelectMenu(
                    custom_id='custom',
                    options=[SelectMenuOption(label='Option 1', value='option_1')],
                ),
            ],
        )


def test_components_can_be_max_5() -> None:
    """Test that components can be a maximum of 5."""
    # fmt: off
    components = [
        ActionRow(components=[
            Button(custom_id=f'button_{i}'),
        ])
        for i in range(6)
    ]
    # fmt: on
    with pytest.raises(ValueError, match='Components must have 5 or fewer action rows'):
        CreateMessageRequest(components=components)


def test_wrap_components_in_action_row() -> None:
    """Test that components are wrapped in an ActionRow."""
    # fmt: off
    components = [
        Button(custom_id=f'button_{i}')
        for i in range(5)
    ]
    # fmt: on

    request = CreateMessageRequest(components=components)

    assert len(request.components) == 1
    assert isinstance(request.components[0], ActionRow)
    assert len(request.components[0].components) == 5
    assert request.components[0].components[0].custom_id == 'button_0'
    assert request.components[0].components[4].custom_id == 'button_4'


class _Container(Protocol):
    components: list[Component] | Component | None


@pytest.mark.parametrize(
    'container',
    [
        CreateMessageRequest,
        UpdateMessageRequest,
        InteractionCreateMessageData,
        InteractionUpdateMessageData,
        ThreadMessage,
    ],
)
def test_wrap_component_to_list_and_action_row(container: _Container) -> None:
    """Test that components are wrapped in an ActionRow."""
    request = container(components=Button(custom_id='button_0'))

    assert len(request.components) == 1
    assert isinstance(request.components[0], ActionRow)
    assert len(request.components[0].components) == 1
    assert request.components[0].components[0].custom_id == 'button_0'


def test_wrap_component_to_list_in_action_row() -> None:
    """Test that components are wrapped in an ActionRow."""
    request = ActionRow(components=[Button(custom_id='button_0')])

    assert len(request.components) == 1
    assert request.components[0].custom_id == 'button_0'


def test_components_cannot_be_empty() -> None:
    """Test that components cannot be empty."""
    with pytest.raises(ValueError):  # noqa: PT011
        ActionRow(components=[])


def test_action_row_can_have_max_5_components() -> None:
    """Test that an ActionRow can have a maximum of 5 components."""
    # fmt: off
    components = [
        ActionRow(components=[
            Button(custom_id=f'button_{i}'),
        ])
        for i in range(6)
    ]
    # fmt: on
    with pytest.raises(ValueError, match='ActionRow must have 5 or fewer components'):
        CreateMessageRequest(components=components)
