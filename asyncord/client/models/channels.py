from __future__ import annotations

import enum
from datetime import datetime

from pydantic import Field, BaseModel, validator

from asyncord.snowflake import Snowflake

from .users import User


class Channel(BaseModel):
    """Channel object.

    Example:
    ::
    {
        "name": "my-category",
        "type": 4,
        "id": 1
    }

    ::
    {
        "name": "naming-things-is-hard",
        "type": 0,
        "id": 2,
        "parent_id": 1
    }

    Read more info at:
    https://discord.com/developers/docs/resources/channel#channel-object
    """

    id: Snowflake
    """channel id"""

    type: ChannelType

    guild_id: Snowflake | None = None
    """The id of the guild.

    May be missing for some channel objects received over gateway guild dispatches.
    """

    position: int | None = None
    """sorting position of the channel"""

    permission_overwrites: list[Overwrite] | None = None
    """explicit permission overwrites for members and roles."""

    name: str | None = Field(None, min_length=1, max_length=100)
    """channel name (2-100 characters)"""

    topic: str | None = Field(min_length=0, max_length=1024)
    """The channel topic(0 - 1024 characters)."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    last_message_id: Snowflake | None = None
    """The id of the last message sent in this channel.

    May not point to an existing or valid message.
    """

    bitrate: int | None = None
    """The bitrate ( in bits) of the voice channel."""

    user_limit: int | None = None
    """The user limit of the voice channel."""

    rate_limit_per_user: int | None = Field(None, min=0, max=21600)
    """Amount of seconds a user has to wait before sending another message(0 - 21600).

    Bots, as well as users with the permission manage_messages or manage_channel,
    are unaffected. `rate_limit_per_user` also applies to thread creation.
    Users can send one message and create one thread during each
    `rate_limit_per_user` interval.
    """

    recipients: list[User] | None = None
    """The recipients of the DM."""

    icon: str | None = None
    """Icon hash."""

    owner_id: Snowflake | None = None
    """ID of the creator of the group DM or thread."""

    application_id: Snowflake | None = None
    """Application id of the group DM creator if it is bot - created."""

    parent_id: Snowflake | None = None
    """Parent category or channel id.

    For guild channels: id of the parent category for a channel.
    for threads:
        id of the text channel this thread was created.
    Each parent category can contain up to 50 channels.
    """

    last_pin_timestamp: datetime | None = None
    """Timestamp when the last pinned message was pinned.

    This may be null in events such as GUILD_CREATE when a message is not pinned.
    """

    rtc_region: str | None = None
    """Voice region id for the voice channel, automatic when set to null."""

    video_quality_mode: int | None = None
    """The camera video quality mode of the voice channel, 1 when not present."""

    message_count: int | None = None
    """An approximate count of messages in a thread, stops counting at 50."""

    member_count: int | None = None
    """An approximate count of users in a thread, stops counting at 50."""

    thread_metadata: ThreadMetadata | None = None
    """Thread - specific fields not needed by other channels."""

    member: ThreadMember | None = None
    """Thread member object for the current user.

    If they have joined the thread, only included on certain API endpoints.
    """

    default_auto_archive_duration: int | None = None
    """Default duration ( in minutes) that the clients (not the API) will use
    for newly created threads.

    To automatically archive the thread after recent activity.
    Can be set to: 60, 1440, 4320, 10080.
    """
    permissions: str | None = None
    """Computed permissions for the invoking user in the channel, including overwrites.

    Only included when part of the resolved data received on a slash command interaction.
    """
    flags: ChannelFlag | None = None
    """Flags for the channel."""

    total_message_sent: int | None = None
    """Number of messages ever sent in a thread.

    It's similar to message_count on message creation, but will not decrement
    the number when a message is deleted.
    """


class ChannelMention(BaseModel):
    """Channel mention object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#channel-mention-object
    """
    id: Snowflake
    """id of the channel"""

    guild_id: Snowflake
    """id of the guild containing the channel"""

    type: ChannelType
    """the type of channel"""

    name: str
    """the name of the channel"""


@enum.unique
class ChannelType(enum.IntEnum):
    GUILD_TEXT = 0
    """A text channel within a server."""

    DM = 1
    """A direct message between users."""

    GUILD_VOICE = 2
    """A voice channel within a server"""

    GROUP_DM = 3
    """A direct message between multiple users"""

    GUILD_CATEGORY = 4
    """An organizational category that contains up to 50 channels."""

    GUILD_ANNOUNCEMENT = 5
    """A channel that users can follow and crosspost into their own server.

    Formerly news channels.
    """

    ANNOUNCEMENT_THREAD = 10
    """A temporary sub-channel within a GUILD_ANNOUNCEMENT channel."""

    GUILD_PUBLIC_THREAD = 11
    """A temporary sub-channel within a GUILD_TEXT channel."""

    GUILD_PRIVATE_THREAD = 12
    """A temporary sub - channel within a `GUILD_TEXT` channel.

    The channel is only viewable by those invited and those with
    the `MANAGE_THREADS` permission.
    """

    GUILD_STAGE_VOICE = 13
    """A voice channel for hosting events with an audience."""

    GUILD_FORUM = 14
    """Channel that can only contain threads."""


@enum.unique
class OverwriteType(enum.IntEnum):
    """Type of overwrite"""
    ROLE = 0
    USER = 1


class Overwrite(BaseModel):
    """https://discord.com/developers/docs/resources/channel#overwrite-object"""
    id: Snowflake
    """Role or user id"""

    type: OverwriteType
    """Either 0 (role) or 1 (member)"""

    allow: str
    """Permission bit set.

    Example:
        66321471
    """
    deny: str
    """Permission bit set

    Example:
        16241572
    """


class ThreadMetadata(BaseModel):
    """https://discord.com/developers/docs/resources/channel#thread-metadata-object"""

    archived: bool
    """Whether the thread is archived."""

    auto_archive_duration: int
    """Duration in minutes to automatically archive the thread after recent activity.

    Can be set to: 60, 1440, 4320, 10080.
    """

    archive_timestamp: datetime
    """Timestamp when the thread's archive status was last changed, used for
    calculating recent activity.
    """

    locked: bool
    """Whether the thread is locked.

    When a thread is locked, only users with `MANAGE_THREADS` can unarchive it.
    """

    invitable: bool | None = None
    """Whether non-moderators can add other non-moderators to a thread.

    Only available on private threads.
    """


class ThreadMember(BaseModel):
    """https://discord.com/developers/docs/resources/channel#thread-member-object"""

    id: Snowflake | None = None
    """The id of the thread.

    These field is ommitted on the member sent within each thread in the `GUILD_CREATE` event.
    More info at https://discord.com/developers/docs/topics/gateway-events#guild-create
    """

    user_id: Snowflake | None = None
    """The id of the user.

    These field is ommitted on the member sent within each thread in the `GUILD_CREATE` event.
    More info at https://discord.com/developers/docs/topics/gateway-events#guild-create
    """

    join_timestamp: datetime
    """The time the current user last joined the thread."""

    flags: int
    """Any user - thread settings, currently only used for notifications."""


@enum.unique
class ChannelFlag(enum.IntFlag):
    """https://discord.com/developers/docs/resources/channel#channel-object-channel-flags"""

    NONE = 0
    """No flags set."""

    PINNED = 1 << 1
    """Whether the channel is pinned."""

    REQUIRE_TAG = 1 << 4
    """whether a tag is required to be specified when creating a thread in a GUILD_FORUM channel.
    Tags are specified in the applied_tags field"""


class ForumTag(BaseModel):
    id: Snowflake
    """the id of the tag"""

    name: str
    """the name of the tag(0 - 20 characters)"""

    moderated: bool
    """whether this tag can only be added to or removed from threads by a member with the MANAGE_THREADS permission"""

    emoji_id: Snowflake | None
    """the id of a guild's custom emoji *"""

    emoji_name: str | None
    """the unicode character of the emoji *"""

    @validator('emoji_id')
    def check_emoji(cls, value, values):
        if value is not None and values.get('emoji_name') is not None:
            raise ValueError('emoji_id and emoji_name cannot be set at the same time')


Channel.update_forward_refs()
