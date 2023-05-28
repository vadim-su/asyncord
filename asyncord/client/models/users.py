from __future__ import annotations

import enum

from pydantic import BaseModel, Field

from asyncord.snowflake import Snowflake


@enum.unique
class UserFlags(enum.IntFlag):
    """https://discord.com/developers/docs/resources/user#user-object-user-flags"""

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


@enum.unique
class PremiumType(enum.IntEnum):
    """Premium types denote the level of premium a user has.

    Visit the Nitro page to learn more:
    https://discord.com/nitro
    """

    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2


class User(BaseModel):
    """https://discord.com/developers/docs/resources/user#user-object

    Example:
    ::
    {
        "id": "80351110224678912",
        "username": "Nelly",
        "discriminator": "1337",
        "avatar": "8342729096ea3675442027381ff50dfe",
        "verified": true,
        "email": "nelly@discord.com",
        "flags": 64,
        "banner": "06c16474723fe537c283b8efa61a30c8",
        "accent_color": 16711680,
        "premium_type": 1,
        "public_flags": 64
    }
    """

    id: Snowflake
    """The user's id."""

    username: str
    """The user's username, not unique across the platform."""

    discriminator: str = Field(min_length=4, max_length=4)
    """The user's 4 - digit discord-tag."""

    avatar: str | None
    """The user's avatar hash."""

    bot: bool | None = None
    """Whether the user belongs to an OAuth2 application."""

    system: bool | None = None
    """Whether the user is an Official Discord System user (part of the urgent message system)"""

    mfa_enabled: bool | None = None
    """Whether the user has two factor enabled on their account."""

    banner: str | None = None
    """The user's banner hash."""

    accent_color: int | None = None
    """The user's banner color encoded as an integer representation of
        hexadecimal color code."""

    locale: str | None = None
    """The user's chosen language option."""

    verified: bool | None = None
    """Whether the email on this account has been verified."""

    email: str | None = None
    "The user's email."

    flags: UserFlags | None = None
    """The flags on a user's account."""

    premium_type: PremiumType | None = None
    """The type of Nitro subscription on a user's account."""

    public_flags: UserFlags | None = None
    """The public flags on a user's account."""
