"""Role models for the client."""

import enum
import typing

from pydantic import BaseModel

from asyncord.base64_image import Base64ImageInput
from asyncord.client.models.permissions import PermissionFlag
from asyncord.color import DEFAULT_COLOR, ColorInput
from asyncord.snowflake import Snowflake


@enum.unique
class RoleFlag(enum.IntFlag):
    """Role Flags

    Reference:
    https://discord.com/developers/docs/topics/permissions#role-object-role-flags
    """

    IN_PROMPT = 1 << 0
    """Role can be selected by members in an onboarding prompt."""


class CreateRoleInput(BaseModel):
    """Data for creating a role."""

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


class RolePositionInput(BaseModel):
    """Data for changing the position of a role."""

    id: Snowflake
    """Role id."""

    position: int | None = None
    """Sorting position of the role."""


class UpdateRoleInput(BaseModel):
    """Data for updating a role."""

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


class RoleTagsOutput(BaseModel):
    """Tags for a role."""

    bot_id: Snowflake | None = None
    """Id of the bot this role belongs to."""

    integration_id: Snowflake | None = None
    """Id of the integration this role belongs to."""

    premium_subscriber: typing.Any = None
    """Whether this is the guild's premium subscriber role."""

# enum and unique


class RoleOutput(BaseModel):
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

    tags: RoleTagsOutput | None = None
    """Role tags."""

    flags: RoleFlag
    """Role flags combined as a bitfield."""
