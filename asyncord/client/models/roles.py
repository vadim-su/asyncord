import typing

from pydantic import BaseModel

from asyncord.typedefs import LikeSnowflake


class CreateRoleData(BaseModel):
    name: str
    """Name of the role."""

    permissions: str | None = None
    "bitwise value of the enabled/disabled permissions. Defaults to @everyone permissions in guild"

    color: int = 0
    """RGB color value of the role. Defaults to 0."""

    hoist: bool = False
    "Whether the role should be displayed separately in the sidebar. Defaults to False."

    icon: str | None = None
    """The role's icon image (if the guild has the ROLE_ICONS feature). Defaults to False."""

    unicode_emoji: str | None = None
    """the role's unicode emoji as a standard emoji(if the guild has the ROLE_ICONS feature).

    Defaults to False.
    """
    mentionable: bool = False
    """Whether the role should be mentionable. Defaults to False."""


class UpdateRoleData(BaseModel):
    name: str | None = None
    """Name of the role."""

    permissions: str | None = None
    "bitwise value of the enabled/disabled permissions. Defaults to @everyone permissions in guild"

    color: int = 0
    """RGB color value of the role. Defaults to 0."""

    hoist: bool = False
    "Whether the role should be displayed separately in the sidebar. Defaults to False."

    icon: str | None = None
    """The role's icon image (if the guild has the ROLE_ICONS feature). Defaults to False."""

    unicode_emoji: str | None = None
    """the role's unicode emoji as a standard emoji(if the guild has the ROLE_ICONS feature).

    Defaults to False.
    """
    mentionable: bool = False
    """Whether the role should be mentionable. Defaults to False."""


class RoleTags(BaseModel):
    bot_id: LikeSnowflake | None = None
    """the id of the bot this role belongs to"""

    integration_id: LikeSnowflake | None = None
    """the id of the integration this role belongs to"""

    premium_subscriber: typing.Any = None
    """whether this is the guild's premium subscriber role"""


class Role(BaseModel):
    id: LikeSnowflake
    """role id"""

    name: str
    """role name"""

    color: int
    """integer representation of hexadecimal color code"""

    hoist: bool
    """if this role is pinned in the user listing"""

    icon: str | None = None
    """role icon hash"""

    unicode_emoji: str | None = None
    """role unicode emoji"""

    position: int
    """position of this role"""

    permissions: str
    """permission bit set"""

    managed: bool
    """whether this role is managed by an integration"""

    mentionable: bool
    """whether this role is mentionable"""

    tags: RoleTags | None = None
    """the tags this role has"""


class RolePosition(BaseModel):
    id: LikeSnowflake
    """role id"""

    position: int | None = None
    """sorting position of the role"""
