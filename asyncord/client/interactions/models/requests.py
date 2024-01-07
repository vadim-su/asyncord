"""This module contains models for interactions and their responses.

Reference:
https://discord.com/developers/docs/interactions/receiving-and-responding#interactions
"""

from typing import Literal, Union, cast

from pydantic import BaseModel, Field, field_validator

from asyncord.client.commands.models.requests import ApplicationCommandOptionChoiceIn
from asyncord.client.interactions.models.common import InteractionResponseType
from asyncord.client.messages.models.common import MessageFlags
from asyncord.client.messages.models.requests.components import ActionRowIn, ComponentIn, TextInputIn
from asyncord.client.messages.models.requests.embeds import EmbedIn
from asyncord.client.messages.models.requests.messages import (
    AllowedMentionsIn,
    AttachedFileIn,
    AttachmentDataIn,
    BaseMessage,
)


class InteractionPongResponseRequest(BaseModel):
    """Interaction response request data for PONG."""

    type: Literal[InteractionResponseType.PONG] = InteractionResponseType.PONG


class IteractionCreateMessageDataIn(BaseMessage):
    """Message response request data.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    tts: bool = False
    """True if this is a TTS message."""

    content: str | None = Field(None, max_length=2000)
    """Message content."""

    embeds: list[EmbedIn] | None = None
    """List of embeds."""

    allowed_mentions: AllowedMentionsIn | None = None
    """Allowed mentions object."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    components: list[ComponentIn] | None = None
    """List of components."""

    files: list[AttachedFileIn] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentDataIn] | None = None
    """Attachment objects with filename and description.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """


class IteractionChannelMessageResponsRequest(BaseModel):
    """Interaction response request data for CHANNEL_MESSAGE_WITH_SOURCE."""

    type: Literal[InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE] = (
        InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE
    )

    data: IteractionCreateMessageDataIn


class IteractionDeferredChannelMessageResponseRequest(BaseModel):
    """Interaction response data for DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE."""

    type: Literal[InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE] = (
        InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
    )

    data: IteractionCreateMessageDataIn


class InteractionUpdateMessageDataIn(BaseModel):
    """Interaction response data for UPDATE_MESSAGE.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    content: str | None = Field(None, max_length=2000)
    """Message content."""

    embeds: list[EmbedIn] | None = None
    """List of embeds."""

    allowed_mentions: AllowedMentionsIn | None = None
    """Allowed mentions object."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    components: list[ComponentIn] | None = None
    """List of components."""

    files: list[AttachedFileIn] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentDataIn] | None = None
    """Attachment objects with filename and description.

    See Uploading Files:
    https://discord.com/developers/docs/reference#uploading-files
    """


class InteractionDeferredUpdateMessageResponseRequest(BaseModel):
    """Interaction response request data for DEFERRED_UPDATE_MESSAGE."""

    type: Literal[InteractionResponseType.DEFERRED_UPDATE_MESSAGE] = (
        InteractionResponseType.DEFERRED_UPDATE_MESSAGE
    )

    data: InteractionUpdateMessageDataIn


class InteractionUpdateMessageResponseRequest(BaseModel):
    """Interaction response request data for UPDATE_MESSAGE."""

    type: Literal[InteractionResponseType.UPDATE_MESSAGE] = (
        InteractionResponseType.UPDATE_MESSAGE
    )

    data: InteractionUpdateMessageDataIn


class InteractionAutocompleteResultDataIn(BaseModel):
    """Autocomplete response request data.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-autocomplete
    """

    choices: list[ApplicationCommandOptionChoiceIn] = Field(min_length=1, max_length=25)
    """List of autocomplete choices."""


class InteractionAutocompleteResponseRequest(BaseModel):
    """Autocomplete response request data."""

    type: Literal[InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT] = (
        InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT
    )

    data: InteractionAutocompleteResultDataIn


class InteractionModalDataIn(BaseModel):
    """Modal response request data.

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

    components: list[ActionRowIn] | list[TextInputIn] = Field(min_length=1, max_length=5)
    """Components that make up the modal.

    Should be between 1 and 5 (inclusive). Only TextInput components are allowed.
    """

    @field_validator('components')
    def validate_components(
        cls, components: list[ActionRowIn] | list[TextInputIn],
    ) -> list[ActionRowIn] | list[TextInputIn]:
        """Validate the components.

        Components should be wrapped in an ActionRow. If it is not, wrap it in one.
        """
        if isinstance(components[0], TextInputIn):
            # If the first component is a TextInput
            # (pydantic garuntees that all components are the same type), wrap it in an ActionRow.
            text_inputs = cast(list[ComponentIn | TextInputIn], components)
            components = [ActionRowIn(components=text_inputs)]

        components = cast(list[ActionRowIn], components)
        for action_row in components:
            for component in action_row.components:
                if not isinstance(component, TextInputIn):
                    raise ValueError('Only TextInput components are allowed.')

        return components


class InteractionModalResponseRequest(BaseModel):
    """Interaction response request data for MODAL."""

    type: Literal[InteractionResponseType.MODAL] = InteractionResponseType.MODAL
    data: InteractionModalDataIn


type InteractionResponseRequestType = Union[
    InteractionPongResponseRequest,
    IteractionChannelMessageResponsRequest,
    IteractionDeferredChannelMessageResponseRequest,
    InteractionDeferredUpdateMessageResponseRequest,
    InteractionUpdateMessageResponseRequest,
    InteractionAutocompleteResponseRequest,
    InteractionModalResponseRequest,
]
"""Collection of all interaction response data models."""
