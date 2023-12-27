"""This module contains models for the message components.

Reference:
https://discord.com/developers/docs/interactions/message-components#message-components
"""

from __future__ import annotations

import enum
from typing import Annotated, Any, Literal, Self
from typing import get_args as get_typing_args

from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator


@enum.unique
class ComponentType(enum.IntEnum):
    """Component types.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#component-object-component-types
    """

    ACTION_ROW = 1
    """Container for other components."""

    BUTTON = 2
    """Button object."""

    STRING_SELECT = 3
    """Select menu for picking from defined text options."""

    TEXT_INPUT = 4
    """Text input object."""

    USER_SELECT = 5
    """Select menu for users."""

    ROLE_SELECT = 6
    """Select menu for roles."""

    MENTIONABLE_SELECT = 7
    """Select menu for mentionables (users and roles)."""

    CHANNEL_SELECT = 8
    """Select menu for channels."""


SelectComponentType = Literal[
    ComponentType.STRING_SELECT,
    ComponentType.USER_SELECT,
    ComponentType.ROLE_SELECT,
    ComponentType.MENTIONABLE_SELECT,
    ComponentType.CHANNEL_SELECT,
]
SELECT_COMPONENT_TYPE_LIST = get_typing_args(SelectComponentType)


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
    """Emoji to be displayed on the button."""

    name: str
    """Name of the emoji."""

    id: int
    """ID of the emoji."""

    animated: bool | None = None
    """Whether the emoji is animated."""


class ButtonStyle(enum.IntEnum):
    """Button styles.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#button-object-button-styles
    """

    PRIMARY = 1
    """Blurple color.

    Reqired `custom_id`.
    """

    SECONDARY = 2
    """Grey color.

    Reqired `custom_id`.
    """

    SUCCESS = 3
    """Green color.

    Reqired `custom_id`.
    """

    DANGER = 4
    """Red color.

    Reqired `custom_id`.
    """

    LINK = 5
    """Grey with a link icon.

    Reqired `url`.
    """


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

    label: str | None = Field(None, max_length=80)
    """Text to be displayed on the button.

    Max 80 characters.
    """

    style: ButtonStyle = ButtonStyle.PRIMARY
    """Style of the button."""

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


class SelectMenu(BaseComponent):
    """Select menu is interactive components that allow users to select options in messages.

    * Select menus must be sent inside an Action Row
    * An ActionRow can contain up to 1 select menu
    * An ActionRow containing a select menu cannot also contain any buttons

    Reference:
    https://discord.com/developers/docs/interactions/message-components#select-menus
    """

    type: SelectComponentType = ComponentType.STRING_SELECT
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

    @field_validator('options')
    def validate_options(
        cls, options: list[SelectMenuOption], field_info: ValidationInfo,
    ) -> list[SelectMenuOption]:
        """Check that `options` is set for `SelectComponentType.STRING_SELECT`."""
        menu_type = field_info.data['type']

        if menu_type is ComponentType.STRING_SELECT and not options:
            raise ValueError('Options is required for `SelectComponentType.STRING_SELECT`')

        if menu_type is not ComponentType.STRING_SELECT and options:
            raise ValueError('Options is allowed only for `SelectComponentType.STRING_SELECT`')

        return options


class TextInputStyle(enum.IntEnum):
    """Text input styles.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#text-inputs-text-input-styles
    """

    SHORT = 1
    """Single-line input."""

    PARAGRAPH = 2
    """Multi-line input."""


class TextInput(BaseComponent):
    """Text inputs are an interactive component that render on modals.

    They can be used to collect short-form or long-form text.
    Can be used in modal interactions only.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#text-inputs
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

    # FIXME: #25 label should be required for TextInput
    # But for response TextInput it is not required (it uses in interaction response)
    label: str = ''
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

    type: Literal[ComponentType.ACTION_ROW] = ComponentType.ACTION_ROW
    """Type of the component."""

    components: list[Component | TextInput]
    """Components in the action row.

    Text input components are not allowed in action rows.
    """

    @field_validator('components')
    def validate_components(cls, components: list[Component | TextInput]) -> list[Component | TextInput]:
        """Check ActionRow components."""
        component_types = [component.type for component in components]
        set_component_types = set(component_types)

        if ComponentType.BUTTON in set_component_types:
            # any select component in components
            if set_component_types & set(SELECT_COMPONENT_TYPE_LIST):
                raise ValueError(
                    'ActionRow containing a select menu cannot also contain buttons',
                )

        select_components = [
            component_type
            for component_type in component_types
            if component_type in SELECT_COMPONENT_TYPE_LIST
        ]
        if len(select_components) > 1:
            raise ValueError('ActionRow can contain only one select menu')

        if component_types.count(ComponentType.BUTTON) > 5:  # noqa: PLR2004
            raise ValueError('ActionRow can contain up to 5 buttons')

        if TextInput in set_component_types and component_types.count(TextInput) != len(component_types):
            raise ValueError('Text input components cannot be mixed with other components')

        return components


Component = Annotated[ActionRow | Button | SelectMenu, Field(discriminator='type')]
