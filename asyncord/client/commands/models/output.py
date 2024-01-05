"""Output models for discord application commands.

Reference:
https://discord.com/developers/docs/interactions/application-commands
"""

from __future__ import annotations

from pydantic import BaseModel

from asyncord.client.commands.models.common import (
    ApplicationCommandType,
    BaseApplicationCommandOption,
    BaseApplicationCommandOptionChoice,
)
from asyncord.client.models.permissions import PermissionFlag
from asyncord.locale import Locale
from asyncord.snowflake import Snowflake


class ApplicationCommandOptionChoiceOutput(BaseApplicationCommandOptionChoice):
    """Application command option choice object.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-choice-structure
    """


class ApplicationCommandOptionOutput(BaseApplicationCommandOption[
        ApplicationCommandOptionChoiceOutput,
        'ApplicationCommandOptionOutput',
    ]
):
    """Application command option object.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    """


class ApplicationCommandOutput(BaseModel):
    """Application command object.

    Reference:
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

    options: list[ApplicationCommandOptionOutput] | None = None
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
