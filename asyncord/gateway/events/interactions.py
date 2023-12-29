"""This module contains models for interaction events."""
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, RootModel

from asyncord.client.models.channel_data import ChannelType
from asyncord.client.models.commands import AppCommandOptionType, ApplicationCommandType
from asyncord.client.models.components import ActionRow, ComponentType, SelectMenuOption
from asyncord.client.models.members import Member
from asyncord.client.models.messages import Attachment, Embed, InteractionType, MessageFlags, MessageType
from asyncord.client.models.permissions import PermissionFlag
from asyncord.client.models.roles import Role
from asyncord.client.models.users import User
from asyncord.gateway.events.base import GatewayEvent
from asyncord.locale import Locale
from asyncord.snowflake import Snowflake


class BaseInteraction(BaseModel):
    """Base interaction object.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    id: Snowflake
    """ID of the interaction."""

    application_id: Snowflake
    """ID of the application this interaction is for."""

    type: InteractionType
    """Type of interaction."""

    guild_id: Snowflake | None = None
    """Guild that the interaction was sent from."""

    channel: dict | None = None
    """Channel that the interaction was sent from."""

    channel_id: Snowflake | None = None
    """Channel that the interaction was sent from."""

    member: Member | None = None
    """Member object for the invoking user, if invoked in a guild."""

    user: User | None = None
    """User object for the invoking user, if invoked in a DM."""

    token: str
    """Continuation token for responding to the interaction."""

    version: Literal[1] = 1
    """Read-only property.

    Always 1.
    """

    message: dict | None = None
    """For components, the message they were attached to."""

    app_permissions: str | None = None
    """Bitwise set of permissions the app or bot has within the channel the interaction was sent from."""

    locale: Locale | None = None
    """Selected language of the invoking user."""

    guild_locale: str | None = None
    """Guild's preferred locale, if invoked in a guild."""


class PingInteraction(BaseInteraction):
    """Represent a ping interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    type: Literal[InteractionType.PING] = InteractionType.PING


class ApplicationCommandInteractionOption(BaseModel):
    """Represent an option of an application command interaction."""

    name: str
    """Name of the parameter."""

    type: AppCommandOptionType
    """Value of application command option type."""

    value: str | int | float | bool | None = None
    """Value of the option resulting from user input."""

    options: list[ApplicationCommandInteractionOption] = Field(default_factory=list)
    """Present if this option is a group or subcommand.

    Value and options can't be set at the same time.
    """

    focused: bool = False
    """True if this option is the currently focused option for autocomplete."""


class ApplicationCommandInteractionMember(BaseModel):
    """Object representing a member of an application command interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-application-command-interaction-data-structure-application-command-interaction-data-resolved
    """

    nick: str | None = None
    """This user's guild nickname."""

    avatar: str | None = None
    """Member's guild avatar hash."""

    roles: list[Snowflake]
    """Array of snowflakes."""

    joined_at: datetime
    """When the user joined the guild."""

    premium_since: datetime | None = None
    """When the user started boosting the guild."""

    pending: bool | None = None
    """Whether the user has not yet passed the guild's Membership Screening requirements."""

    permissions: str | None = None
    """Total permissions of the member in the channel, including overwrites.

    Returned when in the interaction object.
    """

    communication_disabled_until: datetime | None = None
    """When the user's timeout will expire and the user will be able to communicate in the guild again.

    None or a time in the past if the user is not timed out.
    """


class ApplicationCommandInteractionMessage(BaseModel):
    """Represent a message of an application command interaction."""

    id: Snowflake
    """ID of the message."""

    channel_id: Snowflake
    """ID of the channel the message was sent in."""

    type: MessageType
    """Message type."""

    author: User
    """User who sent the message."""

    content: str
    """Content of the message."""

    timestamp: datetime
    """Timestamp of when the message was sent."""

    edited_timestamp: datetime | None = None
    """Timestamp of when the message was last edited."""

    tts: bool
    """Whether the message was sent with text-to-speech enabled."""

    mention_everyone: bool
    """Whether the message mentions everyone."""

    mentions: list[User]
    """Users mentioned in the message."""

    mention_roles: list[Snowflake]
    """Roles mentioned in the message."""

    attachments: list[Attachment]
    """Attachments sent with the message."""

    embeds: list[Embed]
    """Embeds sent with the message."""

    pinned: bool
    """Whether the message is pinned."""

    flags: MessageFlags
    """Message flags."""


class ApplicationCommandInterationChannel(BaseModel):
    """Partial Channel objects only have id, name, type and permissions fields.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-object-channel-structure
    """

    id: Snowflake
    """Channel id."""

    name: str | None
    """Channel name (1-100 characters)"""

    type: ChannelType
    """Type of channel."""

    permissions: PermissionFlag
    """Computed permissions for the invoking user in the channel, including overwrites."""


class ApplicationCommandInterationThread(ApplicationCommandInterationChannel):
    """Partial Thread objects for application resolved data.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-object-channel-structure
    """

    thread_metadata: dict | None
    """Thread-specific fields not needed by other channels."""

    parent_id: Snowflake | None
    """The id of the parent channel if the channel is a thread."""


ApplicationCommandInteractionChannelType = ApplicationCommandInterationChannel | ApplicationCommandInterationThread


class ApplicationCommandResolvedData(BaseModel):
    """Represent the resolved data payload of an application command interaction."""

    users: dict[Snowflake, User] | None = None
    """Map of Snowflakes to user objects.

    If data for a Member is included, data for its corresponding User will also be included.
    """

    members: dict[Snowflake, ApplicationCommandInteractionMember] | None = None
    """Map of Snowflakes to partial member objects."""

    roles: dict[Snowflake, Role] | None = None
    """Map of Snowflakes to role objects."""

    channels: dict[Snowflake, ApplicationCommandInteractionChannelType] | None = None
    """Map of Snowflakes to partial channel objects."""

    messages: dict[Snowflake, ApplicationCommandInteractionMessage] | None = None
    """Map of Snowflakes to partial messages objects."""

    attachments: dict[Snowflake, Attachment] | None = None
    """Map of Snowflakes to attachment objects."""


class ApplicationCommandInteractionData(BaseModel):
    """Represent data payload of an application command interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-application-command-data-structure
    """

    id: Snowflake
    """ID of the invoked command."""

    name: str
    """Name of the invoked command."""

    type: ApplicationCommandType
    """Type of the invoked command."""

    resolved: ApplicationCommandResolvedData | None = None
    """Converted users + roles + channels + attachments."""

    options: list[ApplicationCommandInteractionOption] | None = None
    """Params + values from the user."""

    guild_id: Snowflake | None = None
    """ID of the guild the command is registered to."""

    target_id: Snowflake | None = None
    """ID of the user or message targeted by a user or message command."""


class ApplicationCommandInteraction(BaseInteraction):
    """Represent an application command interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    type: Literal[InteractionType.APPLICATION_COMMAND] = InteractionType.APPLICATION_COMMAND
    """Type of interaction."""

    data: ApplicationCommandInteractionData
    """Command data payload."""


class ApplicationCommandAutocompleteInteraction(BaseInteraction):
    """Represent an autocomplete interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    type: Literal[InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE] = InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE
    """Type of interaction."""

    data: ApplicationCommandInteractionData
    """Command data payload.

    Same as ApplicationCommandInteractionData, but can some resolved fields set to None.
    """


class MessageComponentInteractionData(BaseModel):
    """Represent data payload of a message component interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-message-component-data-structure
    """

    custom_id: str
    """Custom_id of the component."""

    component_type: ComponentType
    """Type of the component."""

    values: list[SelectMenuOption] | None = None
    """Values the user selected."""


class MessageComponentInteraction(BaseInteraction):
    """Represent a message component interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    type: Literal[InteractionType.MESSAGE_COMPONENT] = InteractionType.MESSAGE_COMPONENT
    """Type of interaction."""

    data: MessageComponentInteractionData
    """Message component data payload."""


class ModalSubmitInteractionData(BaseModel):
    """Represent data payload of a modal submit interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-modal-submit-data-structure
    """

    custom_id: str
    """Custom id value of the modal."""

    components: list[ActionRow] | None = None
    """Values submitted by the user."""


class ModalSubmitInteraction(BaseInteraction):
    """Represent a modal submit interaction.

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object
    """

    type: Literal[InteractionType.MODAL_SUBMIT] = InteractionType.MODAL_SUBMIT
    """Type of interaction."""

    data: ModalSubmitInteractionData
    """Modal submit data payload."""


Interaction = Annotated[
    PingInteraction
    | ApplicationCommandInteraction
    | MessageComponentInteraction
    | ApplicationCommandAutocompleteInteraction
    | ModalSubmitInteraction,
    Field(discriminator='type'),
]


class InteractionCreateEvent(GatewayEvent, RootModel[Interaction]):
    """Represents an INTERACTION_CREATE event."""
