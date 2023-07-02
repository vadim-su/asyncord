"""This module contains models for interactions and their responses.

Reference:
https://discord.com/developers/docs/interactions/receiving-and-responding#interactions
"""

import enum
from typing import Literal

from pydantic import BaseModel, Field

from asyncord.client.models.commands import ApplicationCommandOptionChoice
from asyncord.client.models.components import Component
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


class MessageResponseData(BaseMessageData):
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


class AutocompleteResponseData(BaseModel):
    """Autocomplete response data.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-autocomplete
    """

    choices: list[ApplicationCommandOptionChoice] = Field(min_length=1, max_length=25)
    """List of autocomplete choices."""


class ModalSubmitResponseData(BaseModel):
    """Modal submit response data.

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

    components: list[Component] = Field(min_length=1, max_length=5)
    """Components that make up the modal.

    Should be etween 1 and 5 (inclusive)
    """


class InteractionResponseData(BaseModel):
    """Interaction response data object.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object
    """

    type: InteractionResponseType
    data: MessageResponseData | AutocompleteResponseData | ModalSubmitResponseData | None = None
