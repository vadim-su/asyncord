from __future__ import annotations

import enum
from typing import Annotated, Final

from pydantic import BaseModel, Field, FieldValidationInfo, field_validator

from asyncord.client.models.channels import ChannelType
from asyncord.client.models.permissions import PermissionFlag
from asyncord.locale import Locale
from asyncord.snowflake import Snowflake

_APP_COMMAND_NAME_PATTERN: Final[str] = r'^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$'
_NameAnnotation = Annotated[str, Field(min_length=1, max_length=32, pattern=_APP_COMMAND_NAME_PATTERN)]


@enum.unique
class AppCommandOptionType(enum.IntEnum):
    """Type of the command option."""

    SUB_COMMAND = 1
    """Subcommand is a child of a slash command."""

    SUB_COMMAND_GROUP = 2
    """Subcommand group is a child of a slash command."""

    STRING = 3
    """String is a text-based argument."""

    INTEGER = 4
    """Integer is a numerical argument."""

    BOOLEAN = 5
    """Boolean is a true/false argument."""

    USER = 6
    """User is a Discord user argument."""

    CHANNEL = 7
    """Channel is a Discord channel argument."""

    ROLE = 8
    """Role is a Discord role argument."""

    MENTIONABLE = 9
    """Mentionable is a Discord user or role argument."""

    NUMBER = 10
    """Number is a numerical argument."""

    ATTACHMENT = 11
    """Attachment is a Discord attachment object argument."""


@enum.unique
class ApplicationCommandType(enum.IntEnum):
    """Type of the command.

    More info:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-types
    """

    CHAT_INPUT = 1
    """Slash command.

    Text-based command that shows up when a user types /.
    """

    USER = 2
    """UI-based command that shows up when you right click or tap on a user."""

    MESSAGE = 3
    """UI-based command that shows up when you right click or tap on a message."""


class ApplicationCommandOptionChoice(BaseModel):
    """Represents a choice for a Discord application command option."""

    name: str = Field(..., min_length=1, max_length=100)
    """Name of the choice.

    Must be 1-100 characters long.
    """

    name_localizations: dict[Locale, str] | None = None
    """Dictionary of language codes to localized names. Defaults to None."""

    value: str | int | float
    """Value of the choice.

    If the option type is a string, this must be 1-100 characters long.
    """

    @field_validator('value')
    def validate_value(cls, field_value: str | int | float) -> str | int | float:
        """Validates the value field."""
        if isinstance(field_value, str):
            if not (1 >= len(field_value) <= 100):  # noqa: PLR2004
                raise ValueError('Value field must be 1-100 characters long')
        return field_value


class ApplicationCommandOption(BaseModel):
    """Represents an option for a Discord application command.

    Reference:
        https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: AppCommandOptionType
    """Type of option."""

    name: str = Field(..., min_length=1, max_length=32)
    """Name of the option.

    Must be 1-32 characters long.
    """

    name_localizations: dict[Locale, str] | None
    """Dictionary of language codes to localized names."""

    description: str = Field(..., min_length=1, max_length=100)
    """Description of the option.

    Must be 1-100 characters long.
    """

    description_localizations: dict[Locale, str] | None = None
    """Dictionary of language codes to localized descriptions."""

    required: bool = False
    """Indicates whether the option is required. Defaults to False."""

    choices: list[ApplicationCommandOptionChoice] | None = None
    """List of choices for string and number types."""

    options: list[ApplicationCommandOption] | None = None
    """List of options for subcommand and subcommand group types."""

    channel_types: list[ChannelType] | None = None
    """List of available channel types if the option type is a `CHANNEL`."""

    min_value: int | None = None
    """Minimum value for the option if the option type is `INTEGER` or `NUMBER`."""

    max_value: int | None = None
    """Maximum value for the option if the option type is `INTEGER` or `NUMBER`."""

    min_length: int | None = Field(None, ge=0, le=6000)
    """Minimum length for the option if the option type is `STRING`."""

    max_length: int | None = Field(None, ge=0, le=6000)
    """Maximum length for the option if the option type is `STRING`."""

    autocomplete: bool | None = None
    """Whether the option is a custom autocomplete option for `STRING`, `INTEGER`, or `NUMBER` types.

    Options using autocomplete are not confined to only use choices given by the application.
    """

    @field_validator('options')
    def validate_options(
        cls,
        options: list[ApplicationCommandOption] | None,
        field_info: FieldValidationInfo,
    ) -> list[ApplicationCommandOption] | None:
        """Validate options."""
        if options is None:
            return None

        sub_command_types = {AppCommandOptionType.SUB_COMMAND, AppCommandOptionType.SUB_COMMAND_GROUP}

        if field_info.data['type'] not in sub_command_types:
            raise ValueError('Options are only allowed for subcommand and subcommand group types')

        # Required options must be listed before optional options
        options.sort(key=lambda item: item.required, reverse=True)
        return options

    @field_validator('choices')
    def validate_choices(
        cls,
        field_value: list[ApplicationCommandOptionChoice] | None,
        field_info: FieldValidationInfo,
    ) -> list[ApplicationCommandOptionChoice] | None:
        """Validate options."""
        if field_value is None:
            return None

        allowed_types = {
            AppCommandOptionType.STRING,
            AppCommandOptionType.INTEGER,
            AppCommandOptionType.NUMBER,
        }

        if field_info.data['type'] not in allowed_types:
            raise ValueError('Choices field can only be set for string and number types')
        return field_value

    @field_validator('channel_types')
    def validate_channel_types(
        cls, field_value: list[ChannelType] | None, field_info: FieldValidationInfo,
    ) -> list[ChannelType] | None:
        """Validates the channel_types field."""
        if field_value is None:
            return None

        if field_info.data['type'] is not AppCommandOptionType.CHANNEL:
            raise ValueError('Channel types field can only be set for channel type')
        return field_value

    @field_validator('min_value', 'max_value')
    def validate_min_max_value(
        cls, field_value: int | None, field_info: FieldValidationInfo,
    ) -> int | None:
        """Validates the min_value and max_value fields."""
        if field_value is None:
            return None
        if field_info.data['type'] not in {AppCommandOptionType.INTEGER, AppCommandOptionType.NUMBER}:
            raise ValueError('Min and max value fields can only be set for integer and number types')
        return field_value

    @field_validator('min_length', 'max_length')
    def validate_min_max_length(
        cls, field_value: int | None, field_info: FieldValidationInfo,
    ) -> int | None:
        """Validates the min_length and max_length fields."""
        if field_value is None:
            return None

        if field_info.data['type'] is not AppCommandOptionType.STRING:
            raise ValueError('Min and max length fields can only be set for string type')
        return field_value


class CreateApplicationCommandData(BaseModel):
    """Data to create a Discord application command.

    More info:
    https://discord.com/developers/docs/interactions/application-commands#create-global-application-command-json-params
    """

    name: _NameAnnotation
    """Name of the command.

    Must be 1-32 characters long.
    """

    type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT
    """Type of the command. Defaults to `ApplicationCommandType.CHAT_INPUT`."""

    name_localizations: dict[Locale, _NameAnnotation] | None = None
    """Dictionary of language codes to localized names. Defaults to None."""

    description: str = Field(..., min_length=1, max_length=100)
    """Description of the command.

    Must be 1-100 characters long.
    """

    description_localizations: dict[Locale, str] | None = None
    """Dictionary of language codes to localized descriptions. Defaults to None."""

    options: list[ApplicationCommandOption] | None = Field(None, max_length=25)
    """List of options for the command.

    Must be 0-25 long. Defaults to None.
    """

    default_member_permissions: PermissionFlag | None = None
    """Default permissions for members in the guild."""

    dm_permission: bool = True
    """Indicates whether the command is available in DMs with the app.

    Only for globally-scoped commands.
    Defaults to True.
    """

    default_permission: bool | None = True
    """Indicates whether the command is enabled by default when the app is added to a guild

    Not recommended for use as field will soon be deprecated.
    Defaults to true.
    """

    @field_validator('options')
    def validate_options(
        cls, options: list[ApplicationCommandOption] | None, field_info: FieldValidationInfo,
    ) -> list[ApplicationCommandOption] | None:
        """Validate options."""
        if options is None:
            return None

        if field_info.data['type'] is not ApplicationCommandType.CHAT_INPUT:
            raise ValueError('Options are only allowed for CHAT_INPUT commands')

        # Required options must be listed before optional options
        options.sort(key=lambda item: item.required, reverse=True)
        return options


class ApplicationCommand(BaseModel):
    """Represents a Discord application command.

    More info:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object
    """

    id: Snowflake
    """Id of the command."""

    type: ApplicationCommandType
    """Type of the command."""

    application_id: Snowflake
    """Id of the parent application."""

    guild_id: int | None = None
    """Id of the guild the command is in.

    Set to None if the command is global.
    """

    name: str = Field(..., min_length=1, max_length=32)
    """Name of the command.

    Must be 1-32 characters long.
    """

    name_localizations: dict[Locale, str] | None = None
    """Dictionary of language codes to localized names. Defaults to None."""

    description: str | None = None
    """Description for CHAT_INPUT commands.

    Must be 1-100 characters long. Empty string for other types.
    """

    description_localizations: dict[Locale, str] | None = None
    """Dictionary of language codes to localized descriptions. Defaults to None."""

    options: list[ApplicationCommandOption] | None = Field(None, max_length=25)
    """List of options for the command.

    Must be 0-25 long. Defaults to None.
    """

    default_member_permissions: PermissionFlag | None = None
    """Default permissions for members in the guild."""

    dm_permission: bool = True
    """Indicates whether the command is available in DMs with the app.

    Only for globally-scoped commands.
    Defaults to True.
    """

    default_permission: bool | None = True
    """Indicates whether the command is enabled by default when the app is added to a guild

    Not recommended for use as field will soon be deprecated.
    Defaults to true.
    """

    nsfw: bool = False
    """Indicates whether the command is age-restricted. Defaults to False."""

    version: Snowflake
    """Autoincrementing version identifier updated during substantial record changes."""
