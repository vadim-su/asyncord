"""This module contains the models for members."""

from __future__ import annotations

import enum
from datetime import datetime

from pydantic import BaseModel

from asyncord.client.users.models import User
from asyncord.snowflake import Snowflake


class GuildMemberFlags(enum.IntFlag):
    """Guild member flags.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-member-object-guild-member-flags
    """

    NONE = 0
    """No flags set."""

    DID_REJOIN = 1 << 0
    """Member has left and rejoined the guild"""

    COMPLETED_ONBOARDING = 1 << 1
    """Member has completed onboarding"""

    BYPASSES_VERIFICATION = 1 << 2
    """Member is exempt from guild verification requirements"""

    STARTED_ONBOARDING = 1 << 3
    """Member has started onboarding"""


class Member(BaseModel):
    """Represents a member of a guild.

    Reference: 
    https://discord.com/developers/docs/resources/guild#guild-member-object
    """

    user: User | None = None
    """User this guild member represents."""

    nick: str | None = None
    """User's guild nickname"""

    avatar: str | None = None
    """Member's guild avatar hash."""

    roles: list[Snowflake]
    """List of role snowflakes."""

    joined_at: datetime
    """When the user joined the guild."""

    premium_since: datetime | None = None
    """When the user started boosting the guild."""

    deaf: bool
    """Whether the user is deafened in voice channels."""

    mute: bool
    """Whether the user is muted in voice channels."""

    flags: GuildMemberFlags
    """Guild member flags represented as a bit set, defaults to 0"""

    pending: bool | None = None
    """Whether the user has not yet passed the guild's Membership Screening requirements."""

    permissions: str | None = None
    """Total permissions of the member in the channel, including overwrites.

    Returned when in the interaction object.
    """

    communication_disabled_until: datetime | None = None
    """When the user's timeout will expire and the user will be able to communicate in the guild again.

    None or a time in the past if the user is not timed out.
    """


class UpdateMemberData(BaseModel):
    """Represents data to update a member."""

    nick: str | None = None
    """User's nickname."""

    roles: list[Snowflake] | None = None
    """List of role ids the member is assigned MANAGE_ROLES"""

    mute: bool | None = None
    """Whether the user is muted in voice channels.

    Will throw a 400 error if the user is not in a voice channel MUTE_MEMBERS.
    """

    deaf: bool | None = None
    """Whether the user is deafened in voice channels.

    Will throw a 400 error if the user is not in a voice channel DEAFEN_MEMBERS.
    """

    channel_id: Snowflake | None = None
    """ID of channel to move user If they are connected to voice."""

    communication_disabled_until: datetime | None = None
    """When the user's timeout will expire and the user will be able to communicate in the guild again.

    Up to 28 days in the future. Set to None to remove timeout.
    Will throw a 403 error if the user has the ADMINISTRATOR permission
    or is the owner of the guild MODERATE_MEMBERS.
    """
