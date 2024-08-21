"""Module for defining interaction response request models in the asyncord library.

This module contains various classes that define the structure of
different types of interaction responses that a bot can send.
These classes are used to create request models for different types of
interaction responses, such as Pong, Message, Deferred Message,
Update Deferred Message, Autocomplete, and Modal (not all types are enumerated here).

References:
https://discord.com/developers/docs/interactions/receiving-and-responding#interactions
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Annotated, Literal, cast

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from asyncord.client.commands.models.requests import ApplicationCommandOptionChoice
from asyncord.client.interactions.models.common import InteractionResponseType
from asyncord.client.messages.models.common import MessageFlags
from asyncord.client.messages.models.requests.base_message import BaseMessage, ListAttachmentType, SingleAttachmentType
from asyncord.client.messages.models.requests.components import ActionRow, MessageComponentType, TextInput
from asyncord.client.messages.models.requests.components.action_row import RowComponentType
from asyncord.client.messages.models.requests.embeds import Embed
from asyncord.client.messages.models.requests.messages import AllowedMentions

__all__ = (
    'InteractionRespAutocompleteRequest',
    'InteractionRespDeferredMessageRequest',
    'InteractionRespMessageRequest',
    'InteractionRespModalRequest',
    'InteractionRespPongRequest',
    'InteractionRespUpdateDeferredMessageRequest',
    'InteractionRespUpdateMessageRequest',
    'InteractionResponseRequestType',
    'RootInteractionResponse',
)


class InteractionRespPongRequest(BaseModel):
    """A request model for sending a Pong response to an interaction.

    This model is used when the bot needs to respond to an interaction with a Pong message.
    The 'type' field is set to InteractionResponseType.PONG by default.
    """

    type: Literal[InteractionResponseType.PONG] = InteractionResponseType.PONG
    """Type of interaction response.

    Set to InteractionResponseType.PONG by default.
    """


class InteractionRespMessageRequest(BaseMessage):
    """Request model for sending a Message response to an interaction.

    This model is used when the bot needs to respond to an interaction with a Message.
    It inherits from the BaseMessage model and includes validations.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages

    """

    tts: bool | None = None
    """True if this is a TTS message."""

    content: Annotated[str | None, Field(max_length=2000)] = None
    """Message content."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentions | None = None
    """Object specifying which mentions are allowed in the message."""

    flags: Literal[MessageFlags.EPHEMERAL, MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS and MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    components: Sequence[MessageComponentType] | MessageComponentType | None = None
    """List of components included in the message.."""

    attachments: Annotated[
        ListAttachmentType | SingleAttachmentType | None,
        Field(validate_default=True),  # Necessary for the embedded attachment collection
    ] = None
    """List of attachment object.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """


class InteractionRespUpdateMessageRequest(BaseMessage):
    """Request model for updating a Message response to an interaction.

    This model is used when the bot needs to respond to an interaction with an updated Message.
    It inherits from the BaseMessage model and includes validations.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages

    """

    tts: bool | None = None
    """True if this is a TTS message."""

    content: Annotated[str | None, Field(max_length=2000)] = None
    """Message content."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentions | None = None
    """Object specifying which mentions are allowed in the message."""

    flags: Literal[MessageFlags.EPHEMERAL, MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS and MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    components: Sequence[MessageComponentType] | MessageComponentType | None = None
    """List of components included in the message.."""

    attachments: Annotated[
        ListAttachmentType | SingleAttachmentType | None,
        Field(validate_default=True),  # Necessary for the embedded attachment collection
    ] = None
    """List of attachment object.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """


class InteractionRespDeferredMessageRequest(BaseMessage):
    """Request model for creating a deferred message response to an interaction.

    This model is used when the bot needs to respond to an interaction with a deferred Message.
    It inherits from the BaseMessage model and includes validations.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    tts: bool | None = None
    """True if this is a TTS message."""

    content: Annotated[str | None, Field(max_length=2000)] = None
    """Message content."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions object."""

    flags: Literal[MessageFlags.EPHEMERAL, MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS and MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    components: Sequence[MessageComponentType] | MessageComponentType | None = None
    """List of components."""

    attachments: Annotated[
        ListAttachmentType | SingleAttachmentType | None,
        Field(validate_default=True),  # Necessary for the embedded attachment collection
    ] = None
    """List of attachment object.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """


class InteractionRespUpdateDeferredMessageRequest(BaseMessage):
    """Request model for updating a deferred message response to an interaction.

    This model is used when the bot needs to update a previously
    sent deferred Message in response to an interaction.
    It inherits from the BaseMessage model and includes validations.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-messages
    """

    content: Annotated[str | None, Field(max_length=2000)] = None
    """Message content."""

    embeds: Annotated[Embed | list[Embed], list[Embed], Field(max_length=10)] | None = None
    """Embedded rich content."""

    allowed_mentions: AllowedMentions | None = None
    """Allowed mentions object."""

    flags: Literal[MessageFlags.SUPPRESS_EMBEDS] | None = None
    """Flags to use when sending the message.

    Only MessageFlags.SUPPRESS_EMBEDS can be set.
    """

    components: Sequence[MessageComponentType] | MessageComponentType | None = None
    """List of components."""

    attachments: Annotated[
        ListAttachmentType | SingleAttachmentType | None,
        Field(validate_default=True),  # Necessary for the embedded attachment collection
    ] = None
    """List of attachment object.

    Reference:
    https://discord.com/developers/docs/reference#uploading-files
    """


class InteractionRespAutocompleteRequest(BaseModel):
    """Request model for sending an Autocomplete response to an interaction.

    This model is used when the bot needs to respond to an interaction with an Autocomplete message.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-autocomplete
    """

    choices: list[ApplicationCommandOptionChoice] = Field(max_length=25)
    """List of autocomplete choices."""


class InteractionRespModalRequest(BaseModel):
    """Request model for sending modal popup interaction response.

    This model is used when the bot needs to respond to an interaction with modal popup.

    References:
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-modal
    """

    custom_id: str = Field(max_length=100)
    """Developer - defined identifier for the modal.

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
            text_inputs = cast(Sequence[RowComponentType], components)
            components = [ActionRow(text_inputs)]

        components = cast(list[ActionRow], components)
        for action_row in components:
            for component in action_row.components:
                if not isinstance(component, TextInput):
                    raise ValueError('Only TextInput components are allowed.')

        return components


type InteractionResponseRequestType = (
    InteractionRespPongRequest
    | InteractionRespMessageRequest
    | InteractionRespUpdateMessageRequest
    | InteractionRespDeferredMessageRequest
    | InteractionRespUpdateDeferredMessageRequest
    | InteractionRespAutocompleteRequest
    | InteractionRespModalRequest
)
"""Type of interaction response request data.

This type is a union of several different interaction response request models.
It is used in the `_RootInteractionResponse` class to represent the `data` field,
which can be any of these types depending on the type of interaction response.

The possible types are:
- InteractionRespPongRequest: A request model for sending a Pong response
    to an interaction.
- InteractionRespMessageRequest: A request model for sending a Message response
    to an interaction.
- InteractionRespDeferredMessageRequest: A request model for sending a deferred
    Message response to an interaction.
- InteractionRespUpdateDeferredMessageRequest: A request model for updating
    a deferred Message response to an interaction.
- InteractionRespAutocompleteRequest: A request model for sending an Autocomplete
    response to an interaction.
- InteractionRespModalRequest: A request model for sending a Modal interaction response.
"""


class RootInteractionResponse(BaseModel):
    """Root interaction response request data.

    This model represents the root of an interaction response request. In general only
    for internal use.
    """

    data: InteractionResponseRequestType
    """Interaction response data."""

    type: Annotated[InteractionResponseType | None, Field(validate_default=True)] = None
    """Interaction response type.

    This field always has a value, but it is not required to be provided.
    """

    @field_validator('type', mode='before')
    @classmethod
    def validate_type(
        cls,
        type_value: int | InteractionResponseType | None,
        field_info: ValidationInfo,
    ) -> InteractionResponseType:
        """Validate the type of interaction response request.

        If type is not provided, extract it from data.
        """
        if type_value is not None:
            type_value = InteractionResponseType(type_value)

        data_value = cast(InteractionResponseRequestType, field_info.data.get('data'))
        calculated_type = cls._calculate_data_type(data_value)

        if type_value is None:
            return calculated_type

        if type_value != calculated_type:
            raise ValueError('Provided type is not valid for the given data')

        # type was set correctly by user, just return it
        # it's very rare event that we reach here
        # because user shouldn't set type of root model and shouldn't use it in general
        return type_value

    @classmethod
    def _calculate_data_type(cls, data_value: InteractionResponseRequestType) -> InteractionResponseType:
        """Calculate the type of interaction response request."""
        calculated_type = None

        match data_value:
            case InteractionRespMessageRequest():
                calculated_type = InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE
            case InteractionRespUpdateMessageRequest():
                calculated_type = InteractionResponseType.UPDATE_MESSAGE
            case InteractionRespDeferredMessageRequest():
                calculated_type = InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
            case InteractionRespUpdateDeferredMessageRequest():
                calculated_type = InteractionResponseType.DEFERRED_UPDATE_MESSAGE
            case InteractionRespAutocompleteRequest():
                calculated_type = InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT
            case InteractionRespModalRequest():
                calculated_type = InteractionResponseType.MODAL
            case _:
                raise ValueError('Invalid interaction response data')

        return calculated_type
