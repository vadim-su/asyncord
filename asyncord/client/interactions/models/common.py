"""Common models for interactions."""

import enum


@enum.unique
class InteractionType(enum.IntEnum):
    """Type of interaction.

    Reference:
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

    PREMIUM_REQUIRED = 10
    """Respond to an interaction with an upgrade button.

    Only available for apps with monetization enabled.
    """
