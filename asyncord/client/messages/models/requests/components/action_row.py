"""This module defines the `ActionRow` class, which groups components in a row.

References:
    https://discord.com/developers/docs/interactions/message-components#action-rows
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from typing import Annotated, Literal
from typing import get_args as get_typing_args

from pydantic import Field, field_validator

from asyncord.client.messages.models.common import ComponentType, SelectComponentType
from asyncord.client.messages.models.requests.components.base import BaseComponent
from asyncord.client.messages.models.requests.components.buttons import ButtonComponentType
from asyncord.client.messages.models.requests.components.selects import SelectMenu
from asyncord.client.messages.models.requests.components.text_input import TextInput

SELECT_COMPONENT_TYPE_LIST = get_typing_args(SelectComponentType)
"""List of select component types."""


class ActionRow(BaseComponent):
    """ActionRow is a non-interactive container component for other types of components.

    * You can have up to 5 Action Rows per message
    * ActionRow cannot contain another ActionRow
    * ActionRow can contain only one select menu
    * ActionRow containing a select menu cannot also contain buttons
    * ActionRow can contain up to 5 buttons

    Reference:
    https://discord.com/developers/docs/interactions/message-components#action-rows
    """

    def __init__(
        self,
        components: Sequence[RowComponentType] | RowComponentType,
    ) -> None:
        """Create a new action row.

        This constructor helps to avoid us to add extra indentation in the code.
        By default `components` is a required field (it's a base behavior of pydantic),
        so we can't create an action row without components:
        ```py
        ActionRow(
            components=[
                Button(
                    style=ButtonStyle.SUCCESS,
                    label='Button',
                    custom_id=f'button',
                ),
            ],
        )
        ```
        But after this change we can create an action row without components:
        ```py
        ActionRow([
            Button(
                style=ButtonStyle.SUCCESS,
                label='Button',
                custom_id=f'button',
            ),
        ])
        ```
        That makes the code more readable and clean.

        Args:
            components: Components in the action row.
        """
        super().__init__(components=components)  # type: ignore

    type: Literal[ComponentType.ACTION_ROW] = ComponentType.ACTION_ROW  # type: ignore
    """Type of the component."""

    components: Annotated[Sequence[RowComponentType], Field(min_length=1, max_length=5)] | RowComponentType
    """Components in the action row.

    Text input components are not allowed in action rows.
    """

    @field_validator('components')
    def validate_components(
        cls,
        components: Sequence[RowComponentType] | RowComponentType,
    ) -> Sequence[RowComponentType]:
        """Validate the components in the action row."""
        if not isinstance(components, Sequence):
            components = [components]

        component_counts = Counter(component.type for component in components)

        # Calculate the count of select components
        # fmt: off
        select_component_count = sum(
            count
            for component, count in component_counts.items()
            if component in SELECT_COMPONENT_TYPE_LIST
        )
        # fmt: on

        # Check if BUTTON and any select component are in the same set
        if component_counts[ComponentType.BUTTON] and select_component_count:
            raise ValueError('ActionRow containing a select menu cannot also contain buttons')

        # Check if there are more than one select components
        if select_component_count > 1:
            raise ValueError('ActionRow can contain only one select menu')

        # Check if TextInputInput is mixed with other components
        text_input_count = component_counts[ComponentType.TEXT_INPUT]
        if text_input_count and len(components) != text_input_count:
            raise ValueError('Text input components cannot be mixed with other components')

        return components


type MessageComponentType = Annotated[ActionRow | ButtonComponentType | SelectMenu, Field(discriminator='type')]
"""Type hint for the message component type.

It doens't include `TextInput` because it's not a general component.
It can be used only in modals and accepted only in `ActionRow` components.
"""

type RowComponentType = MessageComponentType | TextInput
"""Type hint for the message component type with text input.

General use case for the ActionRow components.
"""

ActionRow.model_rebuild()
