"""This module defines models for Discord select menu components using Pydantic for data validation.

References:
    https://discord.com/developers/docs/interactions/message-components#select-menus
"""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.messages.models.common import ComponentType, SelectComponentType
from asyncord.client.messages.models.requests.components.base import BaseComponent
from asyncord.client.messages.models.requests.components.emoji import ComponentEmoji
from asyncord.snowflake import SnowflakeInputType


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

    description: Annotated[str, Field(max_length=100)] | None = None
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

    type: Literal[SelectComponentType] = ComponentType.STRING_SELECT  # type: ignore
    """Type of the component of select menu."""

    custom_id: Annotated[str, Field(max_length=100)] | None = None
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

    placeholder: Annotated[str, Field(max_length=150)] | None = None
    """Placeholder text if nothing is selected; max 150 characters."""

    default_values: list[SelectDefaultValue] | None = None
    """List of default values for auto-populated select menu components.

    It means that you can set default values for 'user', 'role', 'channel' select menu components.
    If you need to set default values for 'string' select menu component,
    you can use `default` field in `SelectMenuOption`.

    Number of default values must be in the range defined by min_values and max_values.
    """

    min_values: Annotated[int, Field(ge=0, le=25)] = 1
    """Minimum number of items that must be chosen; default 1, min 0, max 25."""

    max_values: Annotated[int, Field(ge=0, le=25)] = 1
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
