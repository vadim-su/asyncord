"""This module contains models for the application commands.

Reference:
https://discord.com/developers/docs/interactions/application-commands
"""

from __future__ import annotations

from typing import Annotated, Final, Literal

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.commands.models.common import (
    AppCommandOptionType,
    ApplicationCommandType,
)
from asyncord.client.models.permissions import PermissionFlag
from asyncord.locale import LocaleInputType

__all__ = (
    'ApplicationCommandAttachmentOption',
    'ApplicationCommandBooleanOption',
    'ApplicationCommandChannelOption',
    'ApplicationCommandIntegerOption',
    'ApplicationCommandMentionableOption',
    'ApplicationCommandNumberOption',
    'ApplicationCommandOption',
    'ApplicationCommandOptionChoice',
    'ApplicationCommandRoleOption',
    'ApplicationCommandStringOption',
    'ApplicationCommandSubCommandGroupOption',
    'ApplicationCommandSubCommandOption',
    'ApplicationCommandUserOption',
    'BaseApplicationCommandOption',
    'CreateApplicationCommandRequest',
)


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


class BaseApplicationCommandOption(BaseModel):
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


class ApplicationCommandSubCommandOption(BaseApplicationCommandOption):
    """Represents a SUB_COMMAND type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.SUB_COMMAND] = AppCommandOptionType.SUB_COMMAND  # type: ignore

    options: list[ApplicationCommandOption] | None = None
    """List of options for subcommand and subcommand group types."""


class ApplicationCommandSubCommandGroupOption(BaseApplicationCommandOption):
    """Represents a SUB_COMMAND_GROUP type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.SUB_COMMAND_GROUP] = AppCommandOptionType.SUB_COMMAND_GROUP  # type: ignore

    options: list[ApplicationCommandOption] | None = None
    """List of options for subcommand and subcommand group types."""


class ApplicationCommandStringOption(BaseApplicationCommandOption):
    """Represents a STRING type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.STRING] = AppCommandOptionType.STRING  # type: ignore

    choices: _ChoiceType | None = None
    """List of choices for string and number types.

    Max length is 25.
    """

    min_length: Annotated[int | None, Field(ge=0, le=6000)] = None
    """Minimum length for the option."""

    max_length: Annotated[int | None, Field(ge=0, le=6000)] = None
    """Maximum length for the option."""

    autocomplete: bool | None = None
    """Whether the option is a custom autocomplete option.

    Options using autocomplete are not confined to only use choices given by the application.
    """


class ApplicationCommandIntegerOption(BaseApplicationCommandOption):
    """Represents an INTEGER type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.INTEGER] = AppCommandOptionType.INTEGER  # type: ignore

    choices: _ChoiceType | None = None
    """List of choices for string and number types.

    Max length is 25.
    """

    min_value: int | None = None
    """Minimum value for the option."""

    max_value: int | None = None
    """Maximum value for the option."""

    autocomplete: bool | None = None
    """Whether the option is a custom autocomplete option.

    Options using autocomplete are not confined to only use choices given by the application.
    """


class ApplicationCommandBooleanOption(BaseApplicationCommandOption):
    """Represents a BOOLEAN type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.BOOLEAN] = AppCommandOptionType.BOOLEAN  # type: ignore


class ApplicationCommandUserOption(BaseApplicationCommandOption):
    """Represents a USER type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.USER] = AppCommandOptionType.USER  # type: ignore


class ApplicationCommandChannelOption(BaseApplicationCommandOption):
    """Represents a CHANNEL type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.CHANNEL] = AppCommandOptionType.CHANNEL  # type: ignore

    channel_types: list[ChannelType] | None = None
    """List of available channel types if the option type is a `CHANNEL`."""


class ApplicationCommandRoleOption(BaseApplicationCommandOption):
    """Represents a ROLE type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.ROLE] = AppCommandOptionType.ROLE  # type: ignore


class ApplicationCommandMentionableOption(BaseApplicationCommandOption):
    """Represents a MENTIONABLE type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.MENTIONABLE] = AppCommandOptionType.MENTIONABLE  # type: ignore


class ApplicationCommandNumberOption(BaseApplicationCommandOption):
    """Represents a NUMBER type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.NUMBER] = AppCommandOptionType.NUMBER  # type: ignore

    choices: _ChoiceType | None = None
    """List of choices for string and number types.

    Max length is 25.
    """

    min_value: int | None = None
    """Minimum value for the option."""

    max_value: int | None = None
    """Maximum value for the option."""

    autocomplete: bool | None = None
    """Whether the option is a custom autocomplete option.

    Options using autocomplete are not confined to only use choices given by the application.
    """


class ApplicationCommandAttachmentOption(BaseApplicationCommandOption):
    """Represents an ATTACHMENT type option for a Discord application command.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: Literal[AppCommandOptionType.ATTACHMENT] = AppCommandOptionType.ATTACHMENT  # type: ignore


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
    """Type of the command.

    Defaults to `ApplicationCommandType.CHAT_INPUT`.
    """

    name_localizations: dict[LocaleInputType, _NameAnnotation] | None = None
    """Dictionary of language codes to localized names. Defaults to None."""

    description: _DescriptionAnnotation
    """Description of the command.

    Must be 1-100 characters long.
    """

    description_localizations: dict[LocaleInputType, _DescriptionAnnotation] | None = None
    """Dictionary of language codes to localized descriptions. Defaults to None."""

    options: Annotated[list[ApplicationCommandOption], Field(max_length=25)] | None = None
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
        cls,
        options: list[ApplicationCommandOption] | None,
        field_info: ValidationInfo,
    ) -> list[ApplicationCommandOption] | None:
        """Validate options."""
        if options is None:
            return None

        if field_info.data['type'] is not ApplicationCommandType.CHAT_INPUT:
            raise ValueError('Options are only allowed for CHAT_INPUT commands')

        # Required options must be listed before optional options
        options.sort(key=lambda item: item.required, reverse=True)
        return options


type ApplicationCommandOption = (
    ApplicationCommandSubCommandOption
    | ApplicationCommandSubCommandGroupOption
    | ApplicationCommandStringOption
    | ApplicationCommandIntegerOption
    | ApplicationCommandBooleanOption
    | ApplicationCommandUserOption
    | ApplicationCommandChannelOption
    | ApplicationCommandRoleOption
    | ApplicationCommandMentionableOption
    | ApplicationCommandNumberOption
    | ApplicationCommandAttachmentOption
)


_APP_COMMAND_NAME_PATTERN: Final[str] = r'^[-_\p{L}\p{N}\p{sc=Deva}\p{sc=Thai}]{1,32}$'
"""Pattern for the application command name.

The name must be 1-32 characters long.
It can contain letters, numbers, and the following characters: `-`, `_`.
"""
_NameAnnotation = Annotated[str, Field(min_length=1, max_length=32, pattern=_APP_COMMAND_NAME_PATTERN)]
"""Annotated name field for application commands."""
_DescriptionAnnotation = Annotated[str, Field(min_length=1, max_length=100)]
"""Annotated description field for application commands."""
_ChoiceType = Annotated[list[ApplicationCommandOptionChoice], Field(max_length=25)]
"""Annotated choice type for application commands."""
