from __future__ import annotations

import enum
from typing import Literal, Annotated
from typing import get_args as get_typing_args

from pydantic import Field, BaseModel, validator, root_validator


@enum.unique
class ComponentType(enum.IntEnum):
    """Component types.

    Read more at:
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
    """The type of the component."""

    def __init__(self, **data):
        super().__init__(**data)
        # Add `type` to `__fields_set__` to make `dict(exclude_unset)` work properly.
        # We don't need to set 'type' field because it's already set in a component class,
        # but we need to send it to Discord excluding another unset fields.
        self.__fields_set__.add('type')


class ActionRow(BaseComponent):
    """ActionRow is a non-interactive container component for other types of components.

    * You can have up to 5 Action Rows per message
    * ActionRow cannot contain another ActionRow
    * ActionRow can contain only one select menu
    * ActionRow containing a select menu cannot also contain buttons
    * ActionRow can contain up to 5 buttons

    Read more at:
    https://discord.com/developers/docs/interactions/message-components#action-rows
    """

    type: Literal[ComponentType.ACTION_ROW] = ComponentType.ACTION_ROW
    """The type of the component."""

    components: list[Button | SelectMenu]
    """The components in the action row.

    Text input components are not allowed in action rows.
    """

    @validator('components')
    def validate_components(cls, components):
        """Check ActionRow components."""
        component_types = [component.type for component in components]
        set_component_types = set(component_types)

        if ComponentType.ACTION_ROW in set_component_types:
            raise ValueError('ActionRow cannot contain another ActionRow')

        if ComponentType.BUTTON in set_component_types:
            # any select component in components
            if set_component_types & set(SELECT_COMPONENT_TYPE_LIST):
                raise ValueError('ActionRow containing a select menu cannot also contain buttons')

        select_components = [
            component_type for component_type in component_types
            if component_type in SELECT_COMPONENT_TYPE_LIST
        ]
        if len(select_components) > 1:
            raise ValueError('ActionRow can contain only one select menu')

        if component_types.count(ComponentType.BUTTON) > 5:
            raise ValueError('ActionRow can contain up to 5 buttons')

        return components


class ButtonStyle(enum.IntEnum):
    """Button styles.

    Read more at:
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

    Read more at:
    https://discord.com/developers/docs/interactions/message-components#buttons
    """

    type: Literal[ComponentType.BUTTON] = ComponentType.BUTTON
    """The type of the component.

    Only `ComponentType.BUTTON` is allowed.
    """

    style: ButtonStyle = ButtonStyle.PRIMARY
    """The style of the button."""

    label: str | None = Field(None, max_length=80)
    """The text to be displayed on the button.

    Max 80 characters.
    """

    emoji: ComponentEmoji | None = None
    """The emoji to be displayed on the button."""

    custom_id: str | None = Field(None, max_length=100)
    """Developer-defined identifier for the button.

    Max 100 characters.
    """

    url: str | None = None
    """A URL for link-style buttons."""

    disabled: bool = False
    """Whether the button is disabled."""

    @root_validator
    def check_custom_id_or_url(cls, values):
        """Check that `custom_id` or `url` is set."""

        custom_id = values.get('custom_id')
        url = values.get('url')
        if values.get('style') is ButtonStyle.LINK:
            if custom_id:
                raise ValueError('`custom_id` is not allowed for link-style buttons')
            if not url:
                raise ValueError('`url` is required for link-style buttons')
        else:
            if url:
                raise ValueError('`url` is not allowed for non-link-style buttons')
            if not custom_id:
                raise ValueError('`custom_id` is required for non-link-style buttons.')
        return values


class SelectMenu(BaseComponent):
    """Select menu is interactive components that allow users to select options  in messages.

    * Select menus must be sent inside an Action Row
    * An ActionRow can contain up to 1 select menu
    * An ActionRow containing a select menu cannot also contain any buttons

    Read more at:
    https://discord.com/developers/docs/interactions/message-components#select-menus
    """

    type: SelectComponentType = ComponentType.STRING_SELECT
    """Type of the component of select menu."""

    custom_id: str | None = None
    """Developer-defined identifier for the select menu.

    Max 100 characters.
    """

    options: list[SelectMenuOption] = Field(default_factory=list)
    """The choices in the select menu.

    Only required and allowed for `SelectComponentType.STRING_SELECT`.
    Max 25 options.
    """

    @root_validator
    def validate_options(cls, values):
        """Check that `options` is set for `SelectComponentType.STRING_SELECT`."""
        menu_type = values.get('type')
        options = values.get('options')

        if menu_type is ComponentType.STRING_SELECT:
            if not options:
                raise ValueError('Options is required for `SelectComponentType.STRING_SELECT`')
        else:
            if options:
                raise ValueError('Options is allowed only for `SelectComponentType.STRING_SELECT`')

        return values


class ComponentEmoji(BaseModel):
    """Emoji to be displayed on the button."""

    name: str
    """The name of the emoji."""

    id: int
    """The id of the emoji."""

    animated: bool
    """Whether the emoji is animated."""


class SelectMenuOption(BaseModel):
    """Select menu option."""

    label: str = Field(..., max_length=100)
    """User - facing name of the option.

    Max 100 characters.
    """

    value: str = Field(..., max_length=100)
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


class TextInputStyle(enum.IntEnum):
    """Text input styles.

    Read more at:
    https://discord.com/developers/docs/interactions/message-components#text-inputs-text-input-styles
    """

    SHORT = 1
    """Single-line input."""

    PARAGRAPH = 2
    """Multi-line input."""


class TextInput(BaseComponent):
    """Text inputs are an interactive component that render on modals.

    They can be used to collect short-form or long-form text.

    Read more at:
    https://discord.com/developers/docs/interactions/message-components#text-inputs
    """

    type: Literal[ComponentType.TEXT_INPUT] = ComponentType.TEXT_INPUT
    """The type of the component.

    Only `ComponentType.TEXT_INPUT` is allowed.
    """

    custom_id: str
    """Developer-defined identifier for the text input.

    Max 100 characters.
    """

    style: TextInputStyle = TextInputStyle.SHORT
    """The style of the text input."""

    label: str
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

    # def __init__(self, **data) -> None:
    #     super().__init__(**data)
    #     self.__fields_set__.add('style')

    @root_validator
    def check_length(cls, values):
        min_length = values.get('min_length')
        max_length = values.get('max_length')

        if min_length is not None and max_length is not None:
            if min_length > max_length:
                raise ValueError('`min_length` must be less than or equal to `max_length`')

        return values


Component = Annotated[ActionRow | Button | SelectMenu | TextInput, Field(discriminator='type')]

SelectMenu.update_forward_refs()
ActionRow.update_forward_refs()