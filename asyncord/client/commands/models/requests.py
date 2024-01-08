"""This module contains models for the application commands.

Reference:
https://discord.com/developers/docs/interactions/application-commands
"""

from __future__ import annotations

from typing import Annotated, Final

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.commands.models.common import (
    AppCommandOptionType,
    ApplicationCommandType,
)
from asyncord.client.models.permissions import PermissionFlag
from asyncord.locale import LocaleInputType

_APP_COMMAND_NAME_PATTERN: Final[str] = r'^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$'
_NameAnnotation = Annotated[str, Field(min_length=1, max_length=32, pattern=_APP_COMMAND_NAME_PATTERN)]
_DescriptionAnnotation = Annotated[str, Field(min_length=1, max_length=100)]


class ApplicationCommandOptionChoice(BaseModel):
    """Represents an option choice for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-choice-structure
    """

    name: str = Field(min_length=1, max_length=100)
    """Name of the choice.

    Must be 1-100 characters long.
    """

    name_localizations: dict[LocaleInputType, str] | None = None
    """Dictionary of language codes to localized names. Defaults to None."""

    value: Annotated[str, Field(min_length=1, max_length=100)] | int | float
    """Value of the choice.

    If the option type is a string, this must be 1-100 characters long.
    """


class ApplicationCommandOption(BaseModel):
    """Represents an option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: AppCommandOptionType
    """Type of option."""

    name: str = Field(min_length=1, max_length=32)
    """Name of the option.

    Must be 1-32 characters long.
    """

    description: str = Field(min_length=1, max_length=100)
    """Description of the option.

    Must be 1-100 characters long.
    """

    name_localizations: dict[LocaleInputType, str] | None = None
    """Dictionary of language codes to localized names."""

    description_localizations: dict[LocaleInputType, str] | None = None
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

    @field_validator('choices')
    def validate_choices(
        cls,
        choices: list[ApplicationCommandOptionChoice] | None,
        field_info: ValidationInfo,
    ) -> list[ApplicationCommandOptionChoice] | None:
        """Validate options."""
        if choices is None:
            return None

        allowed_types = {
            AppCommandOptionType.STRING,
            AppCommandOptionType.INTEGER,
            AppCommandOptionType.NUMBER,
        }

        if field_info.data['type'] not in allowed_types:
            raise ValueError('Choices field can only be set for string and number types')
        return choices

    @field_validator('options')
    def validate_options(
        cls,
        options: list[ApplicationCommandOption] | None,
        field_info: ValidationInfo,
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

    @field_validator('channel_types')
    def validate_channel_types(
        cls, channel_types: list[ChannelType] | None, field_info: ValidationInfo,
    ) -> list[ChannelType] | None:
        """Validates the channel_types field."""
        if channel_types is None:
            return None

        if field_info.data['type'] is not AppCommandOptionType.CHANNEL:
            raise ValueError('Channel types field can only be set for channel type')
        return channel_types

    @field_validator('min_value', 'max_value')
    def validate_min_max_value(
        cls, field_value: int | None, field_info: ValidationInfo,
    ) -> int | None:
        """Validates the min_value and max_value fields."""
        if field_value is None:
            return None

        if field_info.data['type'] not in {AppCommandOptionType.INTEGER, AppCommandOptionType.NUMBER}:
            raise ValueError('Min and max value fields can only be set for integer and number types')
        return field_value

    @field_validator('min_length', 'max_length')
    def validate_min_max_length(
        cls, field_value: int | None, field_info: ValidationInfo,
    ) -> int | None:
        """Validates the min_length and max_length fields."""
        if field_value is None:
            return None

        if field_info.data['type'] is not AppCommandOptionType.STRING:
            raise ValueError('Min and max length fields can only be set for string type')
        return field_value


class CreateApplicationCommandRequest(BaseModel):
    """Data to create an application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#create-global-application-command-json-params
    """

    name: _NameAnnotation
    """Name of the command.

    Must be 1-32 characters long.
    """

    type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT
    """Type of the command. Defaults to `ApplicationCommandType.CHAT_INPUT`."""

    name_localizations: dict[LocaleInputType, _NameAnnotation] | None = None
    """Dictionary of language codes to localized names. Defaults to None."""

    description: _DescriptionAnnotation
    """Description of the command.

    Must be 1-100 characters long.
    """

    description_localizations: dict[LocaleInputType, _DescriptionAnnotation] | None = None
    """Dictionary of language codes to localized descriptions. Defaults to None."""

    options: list[ApplicationCommandOption] | None = Field(None, max_length=25)
    """List of options for the command.

    Must be 0-25 long. Defaults to None.
    """

    default_member_permissions: PermissionFlag | None = None
    """Default permissions for members in the guild."""

    dm_permission: bool | None = None
    """Indicates whether the command is available in DMs with the app.

    Only for globally-scoped commands.
    Defaults to True.
    """

    nsfw: bool | None = None
    """Indicates whether the command is age-restricted"""

    @field_validator('options')
    def validate_options(
        cls, options: list[ApplicationCommandOption] | None, field_info: ValidationInfo,
    ) -> list[ApplicationCommandOption] | None:
        """Validate options."""
        if options is None:
            return None

        if field_info.data['type'] is not ApplicationCommandType.CHAT_INPUT:
            raise ValueError('Options are only allowed for CHAT_INPUT commands')

        # Required options must be listed before optional options
        options.sort(key=lambda item: item.required, reverse=True)
        return options
