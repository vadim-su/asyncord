"""This module contains the models for members."""

from __future__ import annotations

import datetime

from pydantic import BaseModel

from asyncord.client.members.models.common import GuildMemberFlags
from asyncord.snowflake import SnowflakeInputType

__all__ = (
    'AddMemberRequest',
    'UpdateMemberRequest',
)


class UpdateMemberRequest(BaseModel):
    """Represents data to update a member.

    Reference:
    https://discord.com/developers/docs/resources/guild#modify-guild-member-json-params
    """

    nick: str | None = None
    """User's nickname."""

    roles: list[SnowflakeInputType] | None = None
    """List of role ids the member is assigned MANAGE_ROLES"""

    mute: bool | None = None
    """Whether the user is muted in voice channels.

    Will throw a 400 error if the user is not in a voice channel MUTE_MEMBERS.
    """

    deaf: bool | None = None
    """Whether the user is deafened in voice channels.

    Will throw a 400 error if the user is not in a voice channel DEAFEN_MEMBERS.
    """

    channel_id: SnowflakeInputType | None = None
    """ID of channel to move user If they are connected to voice."""

    communication_disabled_until: datetime.datetime | None = None
    """When the user's timeout will expire and the user will be able to communicate in the guild again.

    Up to 28 days in the future. Set to None to remove timeout.
    Will throw a 403 error if the user has the ADMINISTRATOR permission
    or is the owner of the guild MODERATE_MEMBERS.
    """

    flags: GuildMemberFlags | None = None
    """Guild member flags represented as a bit set.

    The bot should have MANAGE_GUILD or MANAGE_ROLES or
    (MODERATE_MEMBERS and KICK_MEMBERS and BAN_MEMBERS) permissions.
    """


class AddMemberRequest(BaseModel):
    """Represents data to add a member to a guild.

    Reference:
    https://discord.com/developers/docs/resources/guild#add-guild-member-json-params
    """

    access_token: str
    """Access token for the user."""

    nick: str | None = None
    """Value to set user's nickname to."""

    roles: list[SnowflakeInputType] | None = None
    """List of role ids the member is assigned."""

    mute: bool | None = None
    """Whether the user is muted in voice channels."""

    deaf: bool | None = None
    """Whether the user is deafened in voice channels."""
