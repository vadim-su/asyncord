"""Gateway intents."""

import functools
import operator
from enum import IntFlag, unique


@unique
class Intent(IntFlag):
    """Gateway intents.

    Reference:
    https://discord.com/developers/docs/topics/gateway#gateway-intents
    """

    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_BANS = 1 << 2
    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14
    MESSAGE_CONTENT = 1 << 15
    GUILD_SCHEDULED_EVENTS = 1 << 16
    AUTO_MODERATION_CONFIGURATION = 1 << 20
    AUTO_MODERATION_EXECUTION = 1 << 21


ALL_INTENTS: Intent = functools.reduce(operator.or_, Intent)
"""Set of all available intents."""


DEFAULT_INTENTS = (
    Intent.GUILDS
    | Intent.GUILD_MEMBERS
    | Intent.GUILD_BANS
    | Intent.GUILD_INVITES
    | Intent.GUILD_VOICE_STATES
    | Intent.GUILD_PRESENCES
    | Intent.GUILD_MESSAGES
    | Intent.GUILD_MESSAGE_REACTIONS
    | Intent.GUILD_MESSAGE_TYPING
    | Intent.DIRECT_MESSAGES
    | Intent.DIRECT_MESSAGE_REACTIONS
    | Intent.DIRECT_MESSAGE_TYPING
    | Intent.MESSAGE_CONTENT
    | Intent.GUILD_SCHEDULED_EVENTS
)
"""Set of default intents.

It's lighter than ALL_INTENTS, but not enough. Please use custom intents set instead.
"""
