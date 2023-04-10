from __future__ import annotations

import enum

from pydantic import BaseModel

from asyncord.snowflake import Snowflake


class Interaction(BaseModel):
    """Represents an interaction with a component.

    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    id: Snowflake
    """Interaction id."""

    application_id: Snowflake
    """Application id this interaction is for."""

    type: InteractionType
    """Type of interaction."""

    data: dict

    guild_id: int
    channel_id: int
    member: dict
    token: str
    version: int


@enum.unique
class InteractionType(enum.IntEnum):
    """Type of interaction.

    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-type
    """

    PING = 1
    """Ping interaction."""

    APPLICATION_COMMAND = 2
    """Slash command."""

    MESSAGE_COMPONENT = 3
    """Message component."""

    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    """Autocomplete command."""

    MODAL_SUBMIT = 5
    """Modal submit."""


class ApplicationInteractionData(BaseModel):
    """Represents interaction data.

    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-application-command-data-structure
    """

    id: Snowflake
    """Id of the invoked command."""

    name: str
    """Name of the invoked command."""

    options: list[ApplicationCommandInteractionDataOption]
    """The params + values from the user."""

    resolved: dict
    """Resolved data."""

    custom_id: str
    """Custom id of the component."""

    component_type: ComponentType
    """Type of the component."""

    values: list[str]
    """Values the user selected."""


class ApplicationCommandInteractionDataOption(BaseModel):
    """Represents application command interaction data option.

    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-application-command-data-option-structure
    """

    name: str
    """Name of the parameter."""

    type: ApplicationCommandOptionType
    """The value of the pair."""

    value: str | int | float | None = None  # noqa: WPS110
    """Value of the pair."""

    options: list[ApplicationCommandInteractionDataOption] | None = None
    """Present if this option is a group or subcommand."""

    focused: bool | None = None
    """True if this option is the currently focused option for autocomplete."""


@enum.unique
class ApplicationCommandOptionType(enum.IntEnum):
    """Type of application command option.

    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type
    """

    SUB_COMMAND = 1
    """Subcommand."""

    SUB_COMMAND_GROUP = 2
    """Subcommand group."""

    STRING = 3
    """String."""

    INTEGER = 4
    """Any integer between -2^53 and 2^53."""

    BOOLEAN = 5
    """True or false."""
    USER = 6
    """User object."""

    CHANNEL = 7
    """Includes all channel types + categories."""

    ROLE = 8
    """Role object."""

    MENTIONABLE = 9
    """ Any mentionable object.

    Includes users and roles.
    """

    NUMBER = 10
    """Any double between -2^53 and 2^53."""

    ATTACHMENT = 11
    """Attachment object."""


Interaction.update_forward_refs()
