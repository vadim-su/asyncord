"""This module contains models for the message components.

Reference:
https://discord.com/developers/docs/interactions/message-components#message-components
"""

from __future__ import annotations

from typing import Annotated, Literal, Self
from typing import get_args as get_typing_args

from pydantic import BaseModel, Field, model_validator

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.messages.models.common import ButtonStyle, ComponentType, SelectComponentType, TextInputStyle
from asyncord.snowflake import Snowflake

SELECT_COMPONENT_TYPE_LIST = get_typing_args(SelectComponentType)


class BaseComponentOutput(BaseModel):
    """Base component class."""


class ComponentEmojiOutput(BaseModel):
    """Emoji to be displayed on the button.

    At least one of `name` or `id` must be provided.
    Name is used for unicode emojies,
    Id is a snowflake of custom emojies.
    """

    name: str | None = None
    """Name of the emoji."""

    id: Snowflake | None = None
    """ID of the emoji."""

    animated: bool | None = None
    """Whether the emoji is animated."""

    @model_validator(mode='after')
    def validate_emoji(self) -> Self:
        """Check that `name` or `id` are set."""
        name: str | None = self.name
        id: Snowflake | None = self.id

        if not name and not id:
            raise ValueError('At least one of `name` or `id` must be provided.')

        return self


class ButtonOutput(BaseComponentOutput):
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

    style: ButtonStyle = ButtonStyle.PRIMARY
    """Style of the button."""

    label: str | None = Field(None, max_length=80)
    """Text to be displayed on the button.

    Max 80 characters.
    """

    emoji: ComponentEmojiOutput | None = None
    """Emoji to be displayed on the button."""

    custom_id: str | None = Field(None, max_length=100)
    """Developer-defined identifier for the button.

    Max 100 characters.
    """

    url: str | None = None
    """URL for link-style buttons."""

    disabled: bool = False
    """Whether the button is disabled."""

    @model_validator(mode='after')
    def validate_style(self) -> Self:
        """Check that `custom_id` or `url` are set."""
        custom_id: str | None = self.custom_id
        url: str | None = self.url

        if self.style is ButtonStyle.LINK:
            if custom_id:
                raise ValueError('`custom_id` is not allowed for link-style buttons')
            if not url:
                raise ValueError('`url` is required for link-style buttons')
        else:
            if url:
                raise ValueError('`url` is not allowed for non-link-style buttons')
            if not custom_id:
                raise ValueError('`custom_id` is required for non-link-style buttons.')

        return self


class SelectMenuOptionOutput(BaseModel):
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

    emoji: ComponentEmojiOutput | None = None
    """Emoji to be displayed on the option."""

    default: bool = False
    """Whether the option is shown as selected by default."""


class SelectDefaultValueInput(BaseModel):
    """Select menu default value.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-default-value-structure
    """
    id: Snowflake
    """ID of a user, role, or channel"""

    type: Literal['user', 'role', 'channel']
    """Type of value that id represents. Either user, role, or channel"""


class SelectMenuOutput(BaseComponentOutput):
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

    options: list[SelectMenuOptionOutput] = Field(default_factory=list)
    """Choices in the select menu.

    Only required and allowed for `SelectComponentType.STRING_SELECT`.
    Max 25 options.
    """

    channel_types: list[ChannelType] = Field(default_factory=list)
    """List of channel types to include in the channel select component"""

    placeholder: str | None = None
    """Placeholder text if nothing is selected; max 150 characters."""

    default_values: list[SelectDefaultValueInput] | None = None
    """List of default values for auto-populated select menu components; 
    
    number of default values must be in the range defined by min_values and max_values.
    """

    min_values: int
    """Minimum number of items that must be chosen; default 1, min 0, max 25."""

    max_values: int
    """Maximum number of items that can be chosen; default 1, max 25."""

    disabled: bool = False
    """Whether the select menu is disabled."""


class TextInputOutput(BaseComponentOutput):
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

    style: TextInputStyle = TextInputStyle.SHORT
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


class ActionRowOutput(BaseComponentOutput):
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

    components: list[ComponentOutput | TextInputOutput]
    """Components in the action row.

    Text input components are not allowed in action rows.
    """


ComponentOutput = Annotated[ActionRowOutput | ButtonOutput | SelectMenuOutput, Field(discriminator='type')]
"""Type of the component."""

# Rebuild ActionRow model to add `components` field after Component type created.
ActionRowOutput.model_rebuild()
