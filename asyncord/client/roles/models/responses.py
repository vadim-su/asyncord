"""Role models for the client."""

import enum
from typing import Any

from pydantic import BaseModel

from asyncord.client.models.permissions import PermissionFlag
from asyncord.color import Color
from asyncord.snowflake import Snowflake

__all__ = (
    'RoleFlag',
    'RoleResponse',
    'RoleTagsOut',
)


@enum.unique
class RoleFlag(enum.IntFlag):
    """Role flags.

    Reference:
    https://discord.com/developers/docs/topics/permissions#role-object-role-flags
    """

    IN_PROMPT = 1 << 0
    """Role can be selected by members in an onboarding prompt."""


class RoleTagsOut(BaseModel):
    """Tags for a role."""

    bot_id: Snowflake | None = None
    """Id of the bot this role belongs to."""

    integration_id: Snowflake | None = None
    """Id of the integration this role belongs to."""

    premium_subscriber: Any = None
    """Whether this is the guild's premium subscriber role."""


class RoleResponse(BaseModel):
    """Roles represent a set of permissions attached to a group of users.

    The @everyone role has the same ID as the guild it belongs to.

    Reference:
    https://discord.com/developers/docs/topics/permissions#role-object
    """

    id: Snowflake
    """Role id."""

    name: str
    """Role name."""

    color: Color
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

    tags: RoleTagsOut | None = None
    """Role tags."""

    flags: RoleFlag
    """Role flags combined as a bitfield."""
