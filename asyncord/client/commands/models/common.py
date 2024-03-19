"""Common models for discord application commands.

Reference:
https://discord.com/developers/docs/interactions/application-commands
"""

import enum


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

    Text-based command that shows up when a user types `/`.
    """

    USER = 2
    """UI-based command that shows up when you right click or tap on a user."""

    MESSAGE = 3
    """UI-based command that shows up when you right click or tap on a message."""
