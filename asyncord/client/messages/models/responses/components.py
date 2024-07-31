"""This module contains models for the message components.

Reference:
https://discord.com/developers/docs/interactions/message-components#message-components
"""

from __future__ import annotations

from typing import Annotated, Literal
from typing import get_args as get_typing_args

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel, Field

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.messages.models.common import ButtonStyle, ComponentType, SelectComponentType, TextInputStyle
from asyncord.snowflake import Snowflake

__all__ = (
    'ActionRowOut',
    'BaseComponentOut',
    'ButtonOut',
    'ComponentEmojiOut',
    'ComponentOut',
    'FallbackComponentOut',
    'SelectDefaultValueOut',
    'SelectMenuOptionOut',
    'SelectMenuOut',
    'TextInputOut',
)

SELECT_COMPONENT_TYPE_LIST = get_typing_args(SelectComponentType)


class BaseComponentOut(BaseModel):
    """Base component class."""


class ComponentEmojiOut(BaseModel):
    """Emoji to be displayed on the button.

    At least one of `name` or `id` must be provided.
    Name is used for unicode emojis,
    Id is a snowflake of custom emojis.
    """

    name: str | None = None
    """Name of the emoji."""

    id: Snowflake | None = None
    """ID of the emoji."""

    animated: bool | None = None
    """Whether the emoji is animated."""


class ButtonOut(BaseComponentOut):
    """Buttons are interactive components that render in messages.

    They can be clicked by users, and send an interaction to your app when clicked.

    * Buttons must be sent inside an Action Row
    * An Action Row can contain up to 5 buttons
    * An Action Row containing buttons cannot also contain any select menu components

    Reference:
    https://discord.com/developers/docs/interactions/message-components#buttons
    """

    type: Literal[ComponentType.BUTTON] = ComponentType.BUTTON
    """Type of the component.

    Only `ComponentType.BUTTON` is allowed.
    """

    style: Annotated[ButtonStyle, FallbackAdapter()] = ButtonStyle.PRIMARY
    """Style of the button."""

    label: str | None = None
    """Text to be displayed on the button.

    Max 80 characters.
    """

    emoji: ComponentEmojiOut | None = None
    """Emoji to be displayed on the button."""

    custom_id: str | None = None
    """Developer-defined identifier for the button.

    Max 100 characters.
    """

    url: str | None = None
    """URL for link-style buttons."""

    sku_id: Snowflake | None = None
    """Identifier for a purchasable SKU."""

    disabled: bool = False
    """Whether the button is disabled."""


class SelectMenuOptionOut(BaseModel):
    """Select menu option.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-option-structure
    """

    label: str
    """User - facing name of the option.

    Max 100 characters.
    """

    value: str
    """Value of the option that will be sent to the client.

    Max 100 characters.
    """

    description: str | None = None
    """Additional description of the option.

    Max 100 characters.
    """

    emoji: ComponentEmojiOut | None = None
    """Emoji to be displayed on the option."""

    default: bool = False
    """Whether the option is shown as selected by default."""


class SelectDefaultValueOut(BaseModel):
    """Select menu default value.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-default-value-structure
    """

    id: Snowflake
    """ID of a user, role, or channel"""

    type: Literal['user', 'role', 'channel']
    """Type of value that id represents. Either user, role, or channel"""


class SelectMenuOut(BaseComponentOut):
    """Select menu is interactive components that allow users to select options in messages.

    * Select menus must be sent inside an Action Row
    * An ActionRow can contain up to 1 select menu
    * An ActionRow containing a select menu cannot also contain any buttons

    Reference:
    https://discord.com/developers/docs/interactions/message-components#select-menus
    """

    type: Literal[SelectComponentType] = ComponentType.STRING_SELECT
    """Type of the component of select menu."""

    custom_id: str | None = None
    """Developer-defined identifier for the select menu.

    Max 100 characters.
    """

    options: list[SelectMenuOptionOut] = Field(default_factory=list)
    """Choices in the select menu.

    Only required and allowed for `SelectComponentType.STRING_SELECT`.
    Max 25 options.
    """

    channel_types: list[FallbackAdapter[ChannelType]] = Field(default_factory=list)
    """List of channel types to include in the channel select component."""

    placeholder: str | None = None
    """Placeholder text if nothing is selected; max 150 characters."""

    default_values: list[SelectDefaultValueOut] | None = None
    """List of default values for auto-populated select menu components.

    Number of default values must be in the range defined by min_values and max_values.
    """

    min_values: int
    """Minimum number of items that must be chosen; default 1, min 0, max 25."""

    max_values: int
    """Maximum number of items that can be chosen; default 1, max 25."""

    disabled: bool = False
    """Whether the select menu is disabled."""


class TextInputOut(BaseComponentOut):
    """Text inputs are an interactive component that render on modals.

    They can be used to collect short-form or long-form text.
    Can be used in modal interactions only.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#text-input-object-text-input-structure
    """

    type: Literal[ComponentType.TEXT_INPUT] = ComponentType.TEXT_INPUT
    """Type of the component.

    Only `ComponentType.TEXT_INPUT` is allowed.
    """

    custom_id: str
    """Developer-defined identifier for the text input.

    Max 100 characters.
    """

    style: Annotated[TextInputStyle, FallbackAdapter()] = TextInputStyle.SHORT
    """Style of the text input."""

    label: str | None = None
    """Label of the component."""

    min_length: int | None = None
    """Minimum length of the text input.

    Max 4000 characters.
    """

    max_length: int | None = None
    """Maximum length of the text input.

    Max 4000 characters.
    """

    required: bool = True
    """Whether the text input is required to be filled."""

    value: str | None = None
    """Pre-filled value for this component.

    Max 4000 characters.
    """

    placeholder: str | None = None
    """Placeholder text.

    Max 100 characters.
    """


class ActionRowOut(BaseComponentOut):
    """ActionRow is a non-interactive container component for other types of components.

    * You can have up to 5 Action Rows per message
    * ActionRow cannot contain another ActionRow
    * ActionRow can contain only one select menu
    * ActionRow containing a select menu cannot also contain buttons
    * ActionRow can contain up to 5 buttons

    Reference:
    https://discord.com/developers/docs/interactions/message-components#action-rows
    """

    type: Literal[ComponentType.ACTION_ROW] = ComponentType.ACTION_ROW
    """Type of the component."""

    components: _ConponentList
    """Components in the action row.

    Text input components are not allowed in action rows.
    """


class FallbackComponentOut(BaseComponentOut, extra='allow'):
    """Fallback component type.

    This model is used when the type of the component is unknown.
    """

    type: FallbackAdapter[ComponentType]
    """Type of the component."""

    components: _ConponentList = Field(default_factory=list)
    """Components in the action row.

    Text input components are not allowed in action rows.
    """


ComponentOut = (
    Annotated[
        ActionRowOut | ButtonOut | SelectMenuOut,
        Field(discriminator='type'),
    ]
    | FallbackComponentOut
)
"""Type of the component.

Message Response can contain any of the component types, but not text input.
"""

_ConponentList = list[
    Annotated[
        ActionRowOut | ButtonOut | SelectMenuOut,
        Field(discriminator='type'),
    ]
    | TextInputOut
    | FallbackComponentOut
]
"""Type of the component list.

Similar to `ComponentOut`, but can contain text input.
"""


# Rebuild ActionRow like models to add `components` field after Component type created.
ActionRowOut.model_rebuild()
FallbackComponentOut.model_rebuild()
