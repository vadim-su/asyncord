"""This module contains models for interactions and their responses.

Reference:
https://discord.com/developers/docs/interactions/receiving-and-responding#interactions
"""

from collections.abc import Sequence
from typing import Annotated, Literal, cast

from pydantic import BaseModel, Field, field_validator

from asyncord.client.commands.models.requests import ApplicationCommandOptionChoice
from asyncord.client.interactions.models.common import InteractionResponseType
from asyncord.client.messages.models.common import MessageFlags
from asyncord.client.messages.models.requests.components import ActionRow, Component, TextInput
from asyncord.client.messages.models.requests.embeds import Embed
from asyncord.client.messages.models.requests.messages import (
    AllowedMentions,
    AttachedFile,
    AttachmentData,
    BaseMessage,
)


class InteractionPongResponseRequest(BaseModel):
    """Interaction response request data for PONG."""

    type: Literal[InteractionResponseType.PONG] = InteractionResponseType.PONG


class InteractionCreateMessageData(BaseMessage):
    """Message response request data.

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

    flags: Literal[MessageFlags.EPHEMERAL, MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS and MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    components: Sequence[Component] | Component | None = None
    """List of components."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentData] | None = None
    """Attachment objects with filename and description.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """


class InteractionChannelMessageResponsRequest(BaseModel):
    """Interaction response request data for CHANNEL_MESSAGE_WITH_SOURCE."""

    # fmt: off
    type: Literal[
        InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
    ] = InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE
    # fmt: on

    data: InteractionCreateMessageData


class InteractionDeferredChannelMessageResponseRequest(BaseModel):
    """Interaction response data for DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE."""

    # fmt: off
    type: Literal[
        InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
    ] = InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
    # fmt: on

    data: InteractionCreateMessageData


class InteractionUpdateMessageData(BaseMessage):
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

    components: Sequence[Component] | Component | None = None
    """List of components."""

    files: list[AttachedFile] = Field(default_factory=list, exclude=True)
    """Contents of the file being sent.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """

    attachments: list[AttachmentData] | None = None
    """Attachment objects with filename and description.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """


class InteractionDeferredUpdateMessageResponseRequest(BaseModel):
    """Interaction response request data for DEFERRED_UPDATE_MESSAGE."""

    # fmt: off
    type: Literal[
        InteractionResponseType.DEFERRED_UPDATE_MESSAGE,
    ] = InteractionResponseType.DEFERRED_UPDATE_MESSAGE
    # fmt: on

    data: InteractionUpdateMessageData


class InteractionUpdateMessageResponseRequest(BaseModel):
    """Interaction response request data for UPDATE_MESSAGE."""

    # fmt: off
    type: Literal[
        InteractionResponseType.UPDATE_MESSAGE,
    ] = InteractionResponseType.UPDATE_MESSAGE
    # fmt: on

    data: InteractionUpdateMessageData


class InteractionAutocompleteResultData(BaseModel):
    """Autocomplete response request data.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-autocomplete
    """

    choices: list[ApplicationCommandOptionChoice] = Field(max_length=25)
    """List of autocomplete choices."""


class InteractionAutocompleteResponseRequest(BaseModel):
    """Autocomplete response request data."""

    # fmt: off
    type: Literal[
        InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT,
    ] = InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT
    # fmt: on

    data: InteractionAutocompleteResultData


class InteractionModalData(BaseModel):
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

    components: Annotated[list[ActionRow] | list[TextInput], Field(min_length=1, max_length=5)] | TextInput
    """Components that make up the modal.

    Should be between 1 and 5 (inclusive). Only `TextInput` or `ActionRow` with
    `TextInput` are allowed.
    """

    @field_validator('components')
    def validate_components(
        cls,
        components: list[ActionRow] | list[TextInput],
    ) -> list[ActionRow] | list[TextInput]:
        """Validate the components.

        Components should be wrapped in an ActionRow. If it is not, wrap it in one.
        """
        if not isinstance(components, list):
            components = [components]

        if isinstance(components[0], TextInput):
            # If the first component is a TextInput
            # (pydantic garuntees that all components are the same type), wrap it in an ActionRow.
            text_inputs = cast(list[Component | TextInput], components)
            components = [ActionRow(components=text_inputs)]

        components = cast(list[ActionRow], components)
        for action_row in components:
            for component in action_row.components:
                if not isinstance(component, TextInput):
                    raise ValueError('Only TextInput components are allowed.')

        return components


class InteractionModalResponseRequest(BaseModel):
    """Interaction response request data for MODAL."""

    type: Literal[InteractionResponseType.MODAL] = InteractionResponseType.MODAL
    data: InteractionModalData


type InteractionResponseRequestType = (
    InteractionPongResponseRequest
    | InteractionChannelMessageResponsRequest
    | InteractionDeferredChannelMessageResponseRequest
    | InteractionDeferredUpdateMessageResponseRequest
    | InteractionUpdateMessageResponseRequest
    | InteractionAutocompleteResponseRequest
    | InteractionModalResponseRequest
)
"""Collection of all interaction response data models."""
