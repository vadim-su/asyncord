"""Contains common models for the user module."""

import enum


@enum.unique
class Services(enum.StrEnum):
    """Contains possible servers for the connections.

    Reference:
    https://discord.com/developers/docs/resources/user#connection-object-services
    """

    BATTLENET = 'battlenet'
    BUNGIE = 'bungie'
    DOMAIN = 'domain'
    EBAY = 'ebay'
    EPICGAMES = 'epicgames'
    FACEBOOK = 'facebook'
    GITHUB = 'github'
    INSTAGRAM = 'instagram'
    LEAGUEOFLEGENDS = 'leagueoflegends'
    PAYPAL = 'paypal'
    PLAYSTATION = 'playstation'
    REDDIT = 'reddit'
    RIOTGAMES = 'riotgames'
    SPOTIFY = 'spotify'
    SKYPE = 'skype'
    STEAM = 'steam'
    TIKTOK = 'tiktok'
    TWITCH = 'twitch'
    TWITTER = 'twitter'
    XBOX = 'xbox'
    YOUTUBE = 'youtube'


@enum.unique
class ConnectionVisibilyTypes(enum.IntEnum):
    """Types of connection visibility.

    Reference:
    https://discord.com/developers/docs/resources/user#connection-object-visibility-types
    """

    NONE = 0
    """Invisible to everyone except the user themselves."""

    EVERYONE = 1
    """Visible to everyone."""
