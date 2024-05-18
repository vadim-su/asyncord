"""This module contains models for the message components.

Reference:
https://discord.com/developers/docs/interactions/message-components#message-components
"""

from __future__ import annotations

from collections import Counter
from typing import Annotated, Any, Literal, Self
from typing import get_args as get_typing_args

from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.messages.models.common import ButtonStyle, ComponentType, SelectComponentType, TextInputStyle
from asyncord.snowflake import SnowflakeInputType

SELECT_COMPONENT_TYPE_LIST = get_typing_args(SelectComponentType)
"""List of select component types."""

MAX_BUTTONS_IN_ACTION_ROW = 5
"""Maximum number of buttons in an action row."""


class BaseComponent(BaseModel):
    """Base component class."""

    type: ComponentType
    """Type of the component."""

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        """Initialize the component."""
        super().__init__(**data)
        # Add `type` to `model_fields_set` to make `dict(exclude_unset)` work properly.
        # We don't need to set 'type' field because it's already set in a component class,
        # but we need to send it to Discord excluding another unset fields.
        self.model_fields_set.add('type')


class ComponentEmoji(BaseModel):
    """Emoji to be displayed on the button.

    At least one of `name` or `id` must be provided.
    Name is used for unicode emojis,
    Id is a snowflake of custom emojis.
    """

    name: str | None = None
    """Name of the emoji."""

    id: SnowflakeInputType | None = None
    """ID of the emoji."""

    animated: bool | None = None
    """Whether the emoji is animated."""

    @model_validator(mode='after')
    def name_or_id_required(self) -> Self:
        """Check that `name` or `id` is set."""
        if not self.name and not self.id:
            raise ValueError('At least one of `name` or `id` must be provided')

        return self


class Button(BaseComponent):
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

    emoji: ComponentEmoji | None = None
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


class SelectMenuOption(BaseModel):
    """Select menu option.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-option-structure
    """

    label: str = Field(max_length=100)
    """User - facing name of the option.

    Max 100 characters.
    """

    value: str = Field(max_length=100)
    """Value of the option that will be sent to the client.

    Max 100 characters.
    """

    description: str | None = Field(None, max_length=100)
    """Additional description of the option.

    Max 100 characters.
    """

    emoji: ComponentEmoji | None = None
    """Emoji to be displayed on the option."""

    default: bool = False
    """Whether the option is shown as selected by default."""


class SelectDefaultValue(BaseModel):
    """Select menu default value.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-default-value-structure
    """

    id: SnowflakeInputType
    """ID of a user, role, or channel"""

    type: Literal['user', 'role', 'channel']
    """Type of value that id represents. Either user, role, or channel"""


class SelectMenu(BaseComponent):
    """Select menu is interactive components that allow users to select options in messages.

    * Select menus must be sent inside an Action Row
    * An ActionRow can contain up to 1 select menu
    * An ActionRow containing a select menu cannot also contain any buttons

    Reference:
    https://discord.com/developers/docs/interactions/message-components#select-menus
    """

    type: Literal[SelectComponentType] = ComponentType.STRING_SELECT
    """Type of the component of select menu."""

    custom_id: str | None = Field(None, max_length=100)
    """Developer-defined identifier for the select menu.

    Max 100 characters.
    """

    options: list[SelectMenuOption] = Field(default_factory=list)
    """Choices in the select menu.

    Only required and allowed for `SelectComponentType.STRING_SELECT`.
    Max 25 options.
    """

    channel_types: list[ChannelType] = Field(default_factory=list)
    """List of channel types to include in the channel select component"""

    placeholder: str | None = Field(None, max_length=150)
    """Placeholder text if nothing is selected; max 150 characters."""

    default_values: list[SelectDefaultValue] | None = None
    """List of default values for auto-populated select menu components.

    It means that you can set default values for 'user', 'role', 'channel' select menu components.
    If you need to set default values for 'string' select menu component,
    you can use `default` field in `SelectMenuOption`.

    Number of default values must be in the range defined by min_values and max_values.
    """

    min_values: int = Field(1, ge=0, le=25)
    """Minimum number of items that must be chosen; default 1, min 0, max 25."""

    max_values: int = Field(1, ge=0, le=25)
    """Maximum number of items that can be chosen; default 1, max 25."""

    disabled: bool = False
    """Whether the select menu is disabled."""

    @field_validator('options')
    def validate_options(
        cls,
        options: list[SelectMenuOption],
        field_info: ValidationInfo,
    ) -> list[SelectMenuOption]:
        """Check that `options` is set for `SelectComponentType.STRING_SELECT`."""
        menu_type = field_info.data['type']

        if menu_type is ComponentType.STRING_SELECT and not options:
            raise ValueError('Options is required for `SelectComponentType.STRING_SELECT`')

        if menu_type is not ComponentType.STRING_SELECT and options:
            raise ValueError('Options is allowed only for `SelectComponentType.STRING_SELECT`')

        return options

    @field_validator('channel_types')
    def validate_channel_types(
        cls,
        channel_types: list[ChannelType],
        field_info: ValidationInfo,
    ) -> list[ChannelType]:
        """Check that `channel_types` is set for `SelectComponentType.CHANNEL_SELECT`."""
        menu_type = field_info.data['type']

        if channel_types:
            if menu_type is not ComponentType.CHANNEL_SELECT:
                raise ValueError('Channel types is allowed only for `SelectComponentType.CHANNEL_SELECT`')

        return channel_types

    @field_validator('default_values')
    def validate_default_values(
        cls,
        default_values: list[SelectDefaultValue] | None,
        field_info: ValidationInfo,
    ) -> list[SelectDefaultValue] | None:
        """Check that `default_values` is set for `SelectComponentType.STRING_SELECT`."""
        if not default_values:
            return default_values

        menu_type = field_info.data['type']

        auto_populated_channels = {
            ComponentType.USER_SELECT,
            ComponentType.ROLE_SELECT,
            ComponentType.MENTIONABLE_SELECT,
            ComponentType.CHANNEL_SELECT,
        }

        if menu_type not in auto_populated_channels:
            raise ValueError(f'Channel types is allowed only for {auto_populated_channels}')

        default_values_len = len(default_values)

        if default_values_len > field_info.data['max_values']:
            raise ValueError('Number of default values must be less than or equal to max_values')

        if default_values_len < field_info.data['min_values']:
            raise ValueError('Number of default values must be greater than or equal to min_values')

        return default_values


class TextInput(BaseComponent):
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

    label: str = Field(max_length=45)
    """Label of the component.

    Max 45 characters.
    """

    min_length: int | None = Field(None, ge=0, le=4000)
    """Minimum length of the text input.

    Max 4000 characters.
    """

    max_length: int | None = Field(None, ge=1, le=4000)
    """Maximum length of the text input.

    Max 4000 characters.
    """

    required: bool = True
    """Whether the text input is required to be filled."""

    value: str | None = Field(None, max_length=4000)
    """Pre-filled value for this component.

    Max 4000 characters.
    """

    placeholder: str | None = Field(None, max_length=100)
    """Placeholder text.

    Max 100 characters.
    """

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        """Create a new text input component."""
        super().__init__(**data)  # type: ignore
        self.model_fields_set.add('style')

    @field_validator('max_length')
    def validate_length(cls, max_length: int | None, field_info: ValidationInfo) -> int | None:
        """Validate `min_length` and `max_length`."""
        min_length: int | None = field_info.data['min_length']

        if min_length is not None and max_length is not None:
            if min_length > max_length:
                raise ValueError('`min_length` must be less than or equal to `max_length`')

        return max_length


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

    def __init__(self, components: list[Component | TextInput] | Component | TextInput) -> None:
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
        super().__init__(components=components)

    type: Literal[ComponentType.ACTION_ROW] = ComponentType.ACTION_ROW
    """Type of the component."""

    components: Annotated[list[Component | TextInput], Field(min_length=1, max_length=5)] | Component | TextInput
    """Components in the action row.

    Text input components are not allowed in action rows.
    """

    @field_validator('components')
    def validate_components(
        cls,
        components: list[Component | TextInput] | Component | TextInput,
    ) -> list[Component | TextInput]:
        """Validate the components in the action row."""
        if not isinstance(components, list):
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
        if component_counts[TextInput] and len(components) != component_counts[TextInput]:
            raise ValueError('Text input components cannot be mixed with other components')

        return components


Component = Annotated[ActionRow | Button | SelectMenu, Field(discriminator='type')]
"""Type of the component."""

# Rebuild ActionRow model to add `components` field after Component type created.
ActionRow.model_rebuild()
