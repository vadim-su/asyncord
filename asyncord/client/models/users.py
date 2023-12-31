"""User models for the asyncord client."""

from __future__ import annotations

import enum

from pydantic import BaseModel

from asyncord.color import ColorInput
from asyncord.snowflake import Snowflake


@enum.unique
class UserFlags(enum.IntFlag):
    """User flags.

    Reference:
    https://discord.com/developers/docs/resources/user#user-object-user-flags
    """

    NONE = 0
    """No flags set."""

    STAFF = 1 << 0
    """Discord Employee."""

    PARTNER = 1 << 1
    """Partnered Server Owner."""

    HYPESQUAD = 1 << 2
    """HypeSquad Events Coordinator."""

    BUG_HUNTER_LEVEL_1 = 1 << 3
    """Bug Hunter Level 1."""

    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    """House Bravery Member"""

    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    """House Brilliance Member"""

    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    """House Balance Member."""

    PREMIUM_EARLY_SUPPORTER = 1 << 9
    """Early Nitro Supporter."""

    TEAM_PSEUDO_USER = 1 << 10
    """User is a team.

    More info at:
    https://discord.com/developers/docs/topics/teams
    """

    BUG_HUNTER_LEVEL_2 = 1 << 14
    """Bug Hunter Level 2."""

    VERIFIED_BOT = 1 << 16
    """Verified Bot."""

    VERIFIED_DEVELOPER = 1 << 17
    """Early Verified Bot Developer."""

    CERTIFIED_MODERATOR = 1 << 18
    """Discord Certified Moderator."""

    BOT_HTTP_INTERACTIONS = 1 << 19
    """Bot uses only HTTP interactions and is shown in the online member list.

    More info at:
    https://discord.com/developers/docs/interactions/receiving-and-responding#receiving-an-interaction
    """

    ACTIVE_DEVELOPER = 1 << 22
    """User is an Active Developer

    More info at:
    https://support-dev.discord.com/hc/en-us/articles/10113997751447
    """


@enum.unique
class PremiumType(enum.IntEnum):
    """Premium types denote the level of premium a user has.

    Visit the Nitro page to learn more:
    https://discord.com/nitro

    Reference:
    https://discord.com/developers/docs/game-sdk/users#data-models-premiumtype-enum
    """

    NONE = 0
    """No premium."""

    NITRO_CLASSIC = 1
    """Nitro Classic."""

    NITRO = 2
    """Nitro."""

    NITRO_BASIC = 3
    """Nitro Basic."""


class User(BaseModel):
    """User model representing a Discord user entity.

    Reference:
    https://discord.com/developers/docs/resources/user#user-object
    """

    id: Snowflake
    """User's id."""

    username: str
    """User's username, not unique across the platform."""

    discriminator: str
    """User's 4 - digit discord-tag or 0 if the user has no tag."""

    global_name: str | None
    """User's global name.

    For bots, this is the application name.
    """

    avatar: str | None
    """The user's avatar hash."""

    bot: bool | None = None
    """Whether the user belongs to an OAuth2 application."""

    system: bool | None = None
    """Whether the user is an Official Discord System user (part of the urgent message system)"""

    mfa_enabled: bool | None = None
    """Whether the user has two factor enabled on their account."""

    banner: str | None = None
    """User's banner hash."""

    accent_color: ColorInput | None = None
    """User's banner color encoded as an integer representation of hexadecimal color code."""

    locale: str | None = None
    """User's chosen language option."""

    verified: bool | None = None
    """Whether the email on this account has been verified."""

    email: str | None = None
    """User's email."""

    flags: UserFlags | None = None
    """Flags on a user's account."""

    premium_type: PremiumType | None = None
    """Type of Nitro subscription on a user's account."""

    public_flags: UserFlags | None = None
    """Public flags on a user's account."""

    avatar_decoration: str | None = None
    """User's avatar decoration hash.

    Reference: 
    https://discord.com/developers/docs/reference#image-formatting
    """
