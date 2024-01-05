"""Common models for discord application commands.

Reference:
https://discord.com/developers/docs/interactions/application-commands
"""

from __future__ import annotations

import enum

from pydantic import BaseModel

from asyncord.client.channels.models.common import ChannelType
from asyncord.locale import Locale


@enum.unique
class AppCommandOptionType(enum.IntEnum):
    """Type of the command option.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type
    """

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

    Reference:
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


class BaseApplicationCommandOptionChoice(BaseModel):
    """Choice for a command option.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-choice-structure
    """

    name: str
    """Name of the choice.

    Must be 1-100 characters long.
    """

    name_localizations: dict[Locale, str] | None = None
    """Dictionary of language codes to localized names. Defaults to None."""

    value: str | int | float
    """Value of the choice.

    If the option type is a string, this must be 1-100 characters long.
    """


class BaseApplicationCommandOption[
    CHOICE_T: BaseApplicationCommandOptionChoice,
    OPTION_T: 'BaseApplicationCommandOption',
](BaseModel):
    """Base command option object.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: AppCommandOptionType
    """Type of option."""

    name: str
    """Name of the option."""

    name_localizations: dict[Locale, str] | None = None
    """Dictionary of language codes to localized names."""

    description: str
    """Description of the option.

    Must be 1-100 characters long.
    """

    description_localizations: dict[Locale, str] | None = None
    """Dictionary of language codes to localized descriptions."""

    required: bool = False
    """Indicates whether the option is required. Defaults to False."""

    choices: list[CHOICE_T] | None = None
    """List of choices for string and number types."""

    options: list[OPTION_T] | None = None
    """List of options for subcommand and subcommand group types."""

    channel_types: list[ChannelType] | None = None
    """List of available channel types if the option type is a `CHANNEL`."""

    min_value: int | None = None
    """Minimum value for the option if the option type is `INTEGER` or `NUMBER`."""

    max_value: int | None = None
    """Maximum value for the option if the option type is `INTEGER` or `NUMBER`."""

    min_length: int | None = None
    """Minimum length for the option if the option type is `STRING`."""

    max_length: int | None = None
    """Maximum length for the option if the option type is `STRING`."""

    autocomplete: bool | None = None
    """Whether the option is a custom autocomplete option for `STRING`, `INTEGER`, or `NUMBER` types.

    Options using autocomplete are not confined to only use choices given by the application.
    """
