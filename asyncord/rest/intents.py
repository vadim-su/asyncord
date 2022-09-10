import operator
import functools
from enum import IntFlag, unique
from typing import Annotated


@unique
class Intents(IntFlag):
    """Gateway intents

    You can get more information about intent values and related events by the link:
    https://discord.com/developers/docs/topics/gateway#gateway-intents
    """
    GUILDS = 1 << 0  # noqa: WPS345
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
    GUILD_SCHEDULED_EVENTS = 1 << 16  # it's not a mistake 16 after 14


ALL_INTENTS: Intents = functools.reduce(operator.or_, Intents)
"""Set of all available intents."""


DEFAULT_INTENTS = (
    Intents.GUILDS
    | Intents.GUILD_MEMBERS
    | Intents.GUILD_BANS
    | Intents.GUILD_INVITES
    | Intents.GUILD_VOICE_STATES
    | Intents.GUILD_PRESENCES
    | Intents.GUILD_MESSAGES
    | Intents.GUILD_MESSAGE_REACTIONS
    | Intents.GUILD_MESSAGE_TYPING
    | Intents.DIRECT_MESSAGES
    | Intents.DIRECT_MESSAGE_REACTIONS
    | Intents.DIRECT_MESSAGE_TYPING
    | Intents.GUILD_SCHEDULED_EVENTS
)
"""Set of default intents.

It's lighter than ALL_INTENTS, but not enough. Please use custom intents set instead.
"""
