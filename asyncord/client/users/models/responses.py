"""User models for the asyncord client."""

from __future__ import annotations

import enum
from typing import Any

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel, Field

from asyncord.client.users.models.common import ConnectionVisibilyTypes, Services
from asyncord.color import ColorInput
from asyncord.snowflake import Snowflake

__all__ = (
    'ApplicationRoleConnectionResponse',
    'PremiumType',
    'UserConnectionResponse',
    'UserFlags',
    'UserGuildResponse',
    'UserResponse',
)


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

    Reference:
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

    Reference:
    https://discord.com/developers/docs/interactions/receiving-and-responding#receiving-an-interaction
    """

    ACTIVE_DEVELOPER = 1 << 22
    """User is an Active Developer

    Reference:
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


class UserResponse(BaseModel):
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


class UserGuildResponse(BaseModel):
    """User guild model."""

    id: Snowflake
    """Guild id."""

    name: str
    """Guild name

    Should be 2 - 100 characters, excluding trailing and leading whitespace.
    """

    icon: str | None = None
    """Icon hash."""

    owner: bool | None = None
    """True if the user is the owner of the guild."""

    permissions: str | None = None
    """Total permissions for the user in the guild (excludes overwrites)."""

    features: list[str] = Field(default_factory=list)
    """Strings enabled guild features."""


class UserConnectionResponse(BaseModel):
    """The connection object that the user has attached.

    Reference:
    https://discord.com/developers/docs/resources/user#connection-object-connection-structure
    """

    id: str
    """ID of the connection account."""

    name: str
    """Username of the connection account."""

    type: FallbackAdapter[Services]
    """Service of this connection."""

    revoked: bool | None = None
    """Whether the connection is revoked."""

    # FIXME: No partial integrations example to make model.
    integrations: list[dict[str, Any]] | None = None
    """Array of partial server integrations."""

    verified: bool
    """Whether the connection is verified."""

    friend_sync: bool
    """Whether friend sync is enabled for this connection."""

    show_activity: bool
    """Whether activities related to this connection will be shown in presence updates."""

    two_way_link: bool
    """Whether this connection has a corresponding third party OAuth2 token."""

    visibility: FallbackAdapter[ConnectionVisibilyTypes]
    """Visibility of this connection."""


class ApplicationRoleConnectionResponse(BaseModel):
    """Application role connection object.

    Reference:
    https://discord.com/developers/docs/resources/user#application-role-connection-object-application-role-connection-structure
    """

    platform_name: str | None = None
    """Vanity name of the platform a bot has connected"""

    platform_username: str | None = None
    """Username of the platform a bot has connected"""

    metadata: dict[str, str] | None = None
    """Object mapping application role connection metadata keys to their string-ified value.

    For the user on the platform a bot has connected.
    """
