from collections.abc import Sequence
from typing import Protocol, Self

import pytest

from asyncord.client.interactions.models.requests import (
    InteractionRespMessageRequest,
    InteractionRespUpdateMessageRequest,
)
from asyncord.client.messages.models.requests.components.action_row import ActionRow, MessageComponentType
from asyncord.client.messages.models.requests.components.buttons import (
    AnyButtonWithCustomId,
    DangerButton,
    LinkButton,
    PremiumButton,
    PrimaryButton,
    SecondaryButton,
    SuccessButton,
)
from asyncord.client.messages.models.requests.messages import CreateMessageRequest, UpdateMessageRequest
from asyncord.client.messages.resources import MessageResource
from asyncord.client.threads.models.requests import ThreadMessage


class _Container(Protocol):
    components: Sequence[MessageComponentType] | MessageComponentType | None

    def __call__(self, components: Sequence[MessageComponentType] | MessageComponentType | None) -> Self:  # type: ignore
        """Initialize the container with components."""


@pytest.mark.parametrize(
    'container',
    [
        CreateMessageRequest,
        UpdateMessageRequest,
        InteractionRespMessageRequest,
        InteractionRespUpdateMessageRequest,
        ThreadMessage,
    ],
)
def test_wrap_component_to_list_and_action_row(container: _Container) -> None:
    """Test that components are wrapped in an ActionRow."""
    request = container(
        components=PrimaryButton(
            custom_id='button_0',
            label='Button',
        ),
    )

    assert isinstance(request.components, Sequence)
    assert len(request.components) == 1
    assert isinstance(request.components[0], ActionRow)

    assert isinstance(request.components[0].components, Sequence)
    assert len(request.components[0].components) == 1
    assert not isinstance(request.components[0].components[0], ActionRow)
    assert isinstance(request.components[0].components[0], AnyButtonWithCustomId)
    assert request.components[0].components[0].custom_id == 'button_0'


async def test_create_message_with_buttons(messages_res: MessageResource) -> None:
    """Test creating a message with buttons."""
    components: Sequence[MessageComponentType] = [
        ActionRow([
            PrimaryButton(
                label='Primary',
                custom_id='primary',
            ),
            SecondaryButton(
                label='Secondary',
                custom_id='secondary',
            ),
            SuccessButton(
                label='Success',
                custom_id='success',
            ),
            DangerButton(
                label='Danger',
                custom_id='danger',
            ),
            LinkButton(
                label='Link',
                url='https://discord.com',
            ),
        ]),
    ]
    message = await messages_res.create(
        CreateMessageRequest(
            content='Test message with buttons',
            components=components,
        ),
    )

    try:
        assert message.content == 'Test message with buttons'
        assert isinstance(message.components, Sequence)
        assert len(message.components) == len(components)
    finally:
        await messages_res.delete(message.id)


@pytest.mark.skip(reason='Premium button requires a sku_id which we can not create.')
async def test_create_message_with_premium_button(messages_res: MessageResource) -> None:
    """Test creating a message with premium button."""
    components: Sequence[MessageComponentType] = [
        ActionRow([
            PremiumButton(
                sku_id='42',
            ),
        ]),
    ]
    message = await messages_res.create(
        CreateMessageRequest(
            content='Test message with buttons',
            components=components,
        ),
    )

    try:
        assert message.content == 'Test message with buttons'
        assert isinstance(message.components, Sequence)
        assert len(message.components) == len(components)
    finally:
        await messages_res.delete(message.id)


def test_components_can_be_max_5() -> None:
    """Test that components can be a maximum of 5."""
    # fmt: off
    components = [
        ActionRow([
            PrimaryButton(
                custom_id=f'button_{i}',
                label=f'Button {i}',
            ),
        ])
        for i in range(6)
    ]
    # fmt: on
    with pytest.raises(ValueError, match='Components must have 5 or fewer action rows'):
        CreateMessageRequest(components=components)


def test_wrap_components_in_action_row() -> None:
    """Test that components are wrapped in an ActionRow implicitly."""
    # fmt: off
    components = [
        PrimaryButton(custom_id=f'button_{i}', label=f'Button {i}')
        for i in range(5)
    ]
    # fmt: on

    request = CreateMessageRequest(components=components)

    assert isinstance(request.components, Sequence)
    assert len(request.components) == 1
    assert isinstance(request.components[0], ActionRow)

    assert isinstance(request.components[0].components, Sequence)
    assert len(request.components[0].components) == 5

    assert isinstance(request.components[0].components[0], AnyButtonWithCustomId)
    assert request.components[0].components[0].custom_id == 'button_0'
    assert isinstance(request.components[0].components[4], AnyButtonWithCustomId)
    assert request.components[0].components[4].custom_id == 'button_4'
