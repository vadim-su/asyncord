from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from asyncord.typedefs import LikeSnowflake
from asyncord.snowflake import Snowflake
from asyncord.client.models.users import User


class Member(BaseModel):
    user: User | None = None
    """the user this guild member represents"""

    nick: str | None = None
    """this user's guild nickname"""

    avatar: str | None = None
    """the member's guild avatar hash"""

    roles: list[Snowflake]
    """array of snowflakes"""

    """array of role object ids"""

    joined_at: datetime
    """when the user joined the guild"""

    premium_since: datetime | None = None
    """when the user started boosting the guild"""

    deaf: bool
    """whether the user is deafened in voice channels"""

    mute: bool
    """whether the user is muted in voice channels"""

    pending: bool | None = None
    """whether the user has not yet passed the guild's Membership Screening requirements"""

    permissions: str | None = None
    """Total permissions of the member in the channel, including overwrites.

    Returned when in the interaction object
    """

    communication_disabled_until: datetime | None = None
    """when the user's timeout will expire and the user will be able to communicate in the guild again.

    None or a time in the past if the user is not timed out.
    """


class UpdateMemberData(BaseModel):
    nick: str | None = None
    """value to set user's nickname to MANAGE_NICKNAMES"""

    roles: list[LikeSnowflake] | None = None
    """array of role ids the member is assigned MANAGE_ROLES"""

    mute: bool | None = None
    """whether the user is muted in voice channels.

    Will throw a 400 error if the user is not in a voice channel MUTE_MEMBERS.
    """

    deaf: bool | None = None
    """whether the user is deafened in voice channels.

    Will throw a 400 error if the user is not in a voice channel DEAFEN_MEMBERS.
    """

    channel_id: LikeSnowflake | None = None
    """id of channel to move user to (if they are connected to voice) MOVE_MEMBERS"""

    communication_disabled_until: datetime | None = None
    """when the user's timeout will expire and the user will be able to communicate in the guild again(up to 28 days in the future), set to null to remove timeout. Will throw a 403 error if the user has the ADMINISTRATOR permission or is the owner of the guild MODERATE_MEMBERS"""
