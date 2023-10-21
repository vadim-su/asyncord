"""Role models for the client."""

import typing

from pydantic import BaseModel

from asyncord.base64_image import Base64ImageInput
from asyncord.client.models.permissions import PermissionFlag
from asyncord.color import DEFAULT_COLOR, ColorInput
from asyncord.snowflake import Snowflake


class CreateRoleData(BaseModel):
    name: str
    """Name of the role."""

    permissions: str | None = None
    """Bitwise value of the enabled/disabled permissions.

    Defaults to @everyone permissions in guild
    """

    color: ColorInput = DEFAULT_COLOR
    """RGB color value of the role.

    Defaults to 0.
    """

    hoist: bool = False
    """Whether the role should be displayed separately in the sidebar. Defaults to False."""

    icon: Base64ImageInput | None = None
    """Role's icon image (if the guild has the ROLE_ICONS feature)."""

    unicode_emoji: str | None = None
    """Role's unicode emoji as a standard emoji (if the guild has the ROLE_ICONS feature)."""

    mentionable: bool = False
    """Whether the role should be mentionable.

    Defaults to False.
    """


class UpdateRoleData(BaseModel):
    name: str | None = None
    """Name of the role."""

    permissions: str | None = None
    """Bitwise value of the enabled/disabled permissions.

    Defaults to @everyone permissions in guild.
    """

    color: ColorInput | None = None
    """RGB color value of the role."""

    hoist: bool | None = None
    """Whether the role should be displayed separately in the sidebar.

    Defaults to False.
    """

    icon: str | None = None
    """Role's icon image (if the guild has the ROLE_ICONS feature).

    Defaults to False.
    """

    unicode_emoji: str | None = None
    """Role's unicode emoji as a standard emoji(if the guild has the ROLE_ICONS feature).

    Defaults to False.
    """
    mentionable: bool | None = None
    """Whether the role should be mentionable. Defaults to False."""


class RoleTags(BaseModel):
    bot_id: Snowflake | None = None
    """Id of the bot this role belongs to."""

    integration_id: Snowflake | None = None
    """Id of the integration this role belongs to."""

    premium_subscriber: typing.Any = None
    """Whether this is the guild's premium subscriber role."""


class Role(BaseModel):
    """Roles represent a set of permissions attached to a group of users.

    The @everyone role has the same ID as the guild it belongs to.

    More info at:
    https://discord.com/developers/docs/topics/permissions#role-object
    """

    id: Snowflake
    """Role id."""

    name: str
    """Role name."""

    color: ColorInput
    """Integer representation of hexadecimal color code."""

    hoist: bool
    """Whether this role is pinned in the user listing."""

    icon: str | None = None
    """Role icon hash."""

    unicode_emoji: str | None = None
    """Role unicode emoji."""

    position: int
    """Position of this role in."""

    permissions: PermissionFlag
    """Permission bit set"""

    managed: bool
    """Whether this role is managed by an integration."""

    mentionable: bool
    """Whether this role is mentionable."""

    tags: RoleTags | None = None
    """Role tags."""


class RolePosition(BaseModel):
    id: Snowflake
    """Role id."""

    position: int | None = None
    """Sorting position of the role."""
