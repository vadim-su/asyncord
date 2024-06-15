"""Output models for discord application commands.

Reference:
https://discord.com/developers/docs/interactions/application-commands
"""

from __future__ import annotations

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.commands.models.common import AppCommandOptionType, ApplicationCommandType
from asyncord.client.models.permissions import PermissionFlag
from asyncord.locale import Locale
from asyncord.snowflake import Snowflake

__all__ = (
    'ApplicationCommandOptionChoiceOutput',
    'ApplicationCommandOptionOut',
    'ApplicationCommandResponse',
)


class ApplicationCommandOptionChoiceOutput(BaseModel):
    """Application command option choice object.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-choice-structure
    """

    name: str
    """Name of the choice."""

    name_localizations: dict[Locale, str] | None = None
    """Dictionary of language codes to localized names."""

    value: str | int | float
    """Value of the choice."""


class ApplicationCommandOptionOut(BaseModel):
    """Application command option object.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """

    type: FallbackAdapter[AppCommandOptionType]
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

    choices: list[ApplicationCommandOptionChoiceOutput] | None = None
    """List of choices for string and number types."""

    options: list[ApplicationCommandOptionOut] | None = None
    """List of options for subcommand and subcommand group types."""

    channel_types: list[FallbackAdapter[ChannelType]] | None = None
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


class ApplicationCommandResponse(BaseModel):
    """Application command object.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object
    """

    id: Snowflake
    """Id of the command."""

    type: FallbackAdapter[ApplicationCommandType]
    """Type of the command."""

    application_id: Snowflake
    """Id of the parent application."""

    guild_id: int | None = None
    """Id of the guild the command is in.

    Set to None if the command is global.
    """

    name: str
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

    options: list[ApplicationCommandOptionOut] | None = None
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

    nsfw: bool | None = None
    """Indicates whether the command is age-restricted. Defaults to False."""

    version: Snowflake
    """Autoincrementing version identifier updated during substantial record changes."""
