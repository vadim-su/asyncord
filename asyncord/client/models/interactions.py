"""This module contains models for interactions and their responses.

Reference:
https://discord.com/developers/docs/interactions/receiving-and-responding#interactions
"""

import enum
from typing import Literal, cast

from pydantic import BaseModel, Field, field_validator

from asyncord.client.models.commands import ApplicationCommandOptionChoice
from asyncord.client.models.components import ActionRow, Component, TextInput
from asyncord.client.models.messages import (
    AllowedMentions,
    AttachedFile,
    AttachmentData,
    BaseMessageData,
    Embed,
    MessageFlags,
)


@enum.unique
class InteractionResponseType(enum.IntEnum):
    """Interaction response types.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-type
    """

    PONG = 1
    """ACK a Ping."""

    CHANNEL_MESSAGE_WITH_SOURCE = 4
    """Respond to an interaction with a message."""

    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    """ACK an interaction and edit a response later.

    The user sees a loading state.
    """

    DEFERRED_UPDATE_MESSAGE = 6
    """ACK an interaction and edit the original message later.

    The user does not see a loading state.
    Only valid for component-based interactions.
    """

    UPDATE_MESSAGE = 7
    """Edit the message the component was attached to.

    Only valid for component-based interactions.
    """

    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    """Respond to an autocomplete interaction with suggested choices."""

    MODAL = 9
    """Respond to an interaction with a popup modal."""


class InteractionPongResponseData(BaseModel):
    """Interaction response data for PONG."""

    type: Literal[InteractionResponseType.PONG] = InteractionResponseType.PONG


class IteractionCreateMessageData(BaseMessageData):
    """Message response data.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    tts: bool = False
    """True if this is a TTS message."""

    content: str | None = Field(None, max_length=2000)
    """Message content."""

    embeds: list[Embed] | None = None
    """List of embeds."""

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions object."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    components: list[Component] | None = None
    """List of components."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentData] | None = None
    """Attachment objects with filename and description.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """


class IteractionChannelMessageResponseData(BaseModel):
    """Interaction response data for CHANNEL_MESSAGE_WITH_SOURCE."""

    type: Literal[InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE] = (
        InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE
    )

    data: IteractionCreateMessageData


class IteractionDeferredChannelMessageResponseData(BaseModel):
    """Interaction response data for DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE."""

    type: Literal[InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE] = (
        InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
    )

    data: IteractionCreateMessageData


class InteractionUpdateMessageData(BaseModel):
    """Interaction response data for UPDATE_MESSAGE.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    content: str | None = Field(None, max_length=2000)
    """Message content."""

    embeds: list[Embed] | None = None
    """List of embeds."""

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions object."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    components: list[Component] | None = None
    """List of components."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentData] | None = None
    """Attachment objects with filename and description.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """


class InteractionDeferredUpdateMessageResponseData(BaseModel):
    """Interaction response data for DEFERRED_UPDATE_MESSAGE."""

    type: Literal[InteractionResponseType.DEFERRED_UPDATE_MESSAGE] = (
        InteractionResponseType.DEFERRED_UPDATE_MESSAGE
    )

    data: InteractionUpdateMessageData


class InteractionUpdateMessageResponseData(BaseModel):
    """Interaction response data for UPDATE_MESSAGE."""

    type: Literal[InteractionResponseType.UPDATE_MESSAGE] = (
        InteractionResponseType.UPDATE_MESSAGE
    )

    data: InteractionUpdateMessageData


class InteractionAutocompleteResultData(BaseModel):
    """Autocomplete response data.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-autocomplete
    """

    choices: list[ApplicationCommandOptionChoice] = Field(min_length=1, max_length=25)
    """List of autocomplete choices."""


class InteractionAutocompleteResponseData(BaseModel):
    """Interaction response data for AUTOCOMPLETE."""

    type: Literal[InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT] = (
        InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT
    )

    data: InteractionAutocompleteResultData


class InteractionModalData(BaseModel):
    """Modal response data.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-modal
    """

    custom_id: str = Field(max_length=100)
    """Developer-defined identifier for the modal.

    Max 100 characters.
    """

    title: str = Field(max_length=45)
    """Title of the popup modal.

    Max 45 characters.
    """

    components: list[ActionRow] | list[TextInput] = Field(min_length=1, max_length=5)
    """Components that make up the modal.

    Should be between 1 and 5 (inclusive). Only TextInput components are allowed.
    """

    @field_validator('components')
    def validate_components(cls, components: list[ActionRow] | list[TextInput]) -> list[ActionRow]:
        """Validate the components.

        Components should be wrapped in an ActionRow. If it is not, wrap it in one.
        """
        if isinstance(components, list) and not isinstance(components[0], ActionRow):
            components = [ActionRow(components=components)]

        components = cast(list[ActionRow], components)
        for action_row in components:
            for component in action_row.components:
                if not isinstance(component, TextInput):
                    raise ValueError('Only TextInput components are allowed.')

        return components


class InteractionModalResponseData(BaseModel):
    """Interaction response data for MODAL."""

    type: Literal[InteractionResponseType.MODAL] = InteractionResponseType.MODAL
    data: InteractionModalData


InteractionResponse = (
    InteractionPongResponseData
    | IteractionChannelMessageResponseData
    | IteractionDeferredChannelMessageResponseData
    | InteractionDeferredUpdateMessageResponseData
    | InteractionUpdateMessageResponseData
    | InteractionAutocompleteResponseData
    | InteractionModalResponseData
)
"""Collection of all interaction response data models."""
