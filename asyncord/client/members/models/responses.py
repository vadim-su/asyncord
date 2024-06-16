"""This module contains the response model for a member of a guild."""

import datetime

from pydantic import BaseModel

from asyncord.client.members.models.common import GuildMemberFlags
from asyncord.client.models.permissions import PermissionFlag
from asyncord.client.users.models.responses import UserResponse
from asyncord.snowflake import Snowflake

__all__ = ('MemberResponse',)


class MemberResponse(BaseModel):
    """Represents a member of a guild.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-member-object
    """

    user: UserResponse | None = None
    """User this guild member represents."""

    nick: str | None = None
    """User's guild nickname"""

    avatar: str | None = None
    """Member's guild avatar hash."""

    roles: list[Snowflake]
    """List of role snowflakes."""

    joined_at: datetime.datetime
    """When the user joined the guild."""

    premium_since: datetime.datetime | None = None
    """When the user started boosting the guild."""

    deaf: bool
    """Whether the user is deafened in voice channels."""

    mute: bool
    """Whether the user is muted in voice channels."""

    flags: GuildMemberFlags
    """Guild member flags represented as a bit set, defaults to 0"""

    pending: bool | None = None
    """Whether the user has not yet passed the guild's Membership Screening requirements."""

    permissions: PermissionFlag | None = None
    """Total permissions of the member in the channel, including overwrites.

    Returned when in the interaction object.
    """

    communication_disabled_until: datetime.datetime | None = None
    """When the user's timeout will expire and the user will be able to communicate in the guild again.

    None or a time in the past if the user is not timed out.
    """
