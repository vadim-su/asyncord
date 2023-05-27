"""Channel models for Discord API.

Discord channel documentation starts here:
https://discord.com/developers/docs/resources/channel
"""

from __future__ import annotations

import enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, FieldValidationInfo, field_validator

from asyncord.client.models.users import User
from asyncord.snowflake import Snowflake


@enum.unique
class ChannelType(enum.IntEnum):
    """Channel type.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#channel-object-channel-types
    """

    GUILD_TEXT = 0
    """Text channel within a server."""

    DM = 1
    """Direct message between users."""

    GUILD_VOICE = 2
    """Voice channel within a server."""

    GROUP_DM = 3
    """Direct message between multiple users."""

    GUILD_CATEGORY = 4
    """Organizational category that contains up to 50 channels."""

    GUILD_ANNOUNCEMENT = 5
    """Channel that users can follow and crosspost into their own server.

    Formerly news channels.
    """

    ANNOUNCEMENT_THREAD = 10
    """Temporary sub-channel within a GUILD_ANNOUNCEMENT channel."""

    GUILD_PUBLIC_THREAD = 11
    """Temporary sub-channel within a GUILD_TEXT channel."""

    GUILD_PRIVATE_THREAD = 12
    """Temporary sub-channel within a `GUILD_TEXT` channel.

    The channel is only viewable by those invited and those with
    the `MANAGE_THREADS` permission.
    """

    GUILD_STAGE_VOICE = 13
    """Voice channel for hosting events with an audience."""

    GUILD_DIRECTORY = 14
    """Channel in a hub containing the listed servers."""

    GUILD_FORUM = 15
    """Channel that can only contain threads."""


@enum.unique
class ChannelFlag(enum.IntFlag):
    """Channel flags.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#channel-object-channel-flags
    """

    NONE = 0
    """No flags set."""

    PINNED = 1 << 1
    """Whether the channel is pinned."""

    REQUIRE_TAG = 1 << 4
    """Whether a tag is requiredin a GUILD_FORUM channel.

    Tags are specified in the applied_tags field.
    """


@enum.unique
class OverwriteType(enum.IntEnum):
    """Type of overwrite."""

    ROLE = 0
    USER = 1


class Overwrite(BaseModel):
    """Overwrite object.

    See permissions for more info about `allow` and `deny` fields:
    https://discord.com/developers/docs/topics/permissions#permissions

    Structure defined at:
    https://discord.com/developers/docs/resources/channel#overwrite-object
    """

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
    """Thread metadata object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#thread-metadata-object
    """

    archived: bool
    """Whether the thread is archived."""

    auto_archive_duration: int
    """Duration in minutes to automatically archive the thread after recent activity.

    Can be set to: 60, 1440, 4320, 10080.
    """

    archive_timestamp: datetime
    """Timestamp when the thread's archive status was last changed.

    Used for calculating recent activity.
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
    """Thread member object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#thread-member-object
    """

    id: Snowflake | None = None
    """Thread id.

    These field is ommitted on the member sent within each thread in the `GUILD_CREATE` event.
    More info at https://discord.com/developers/docs/topics/gateway-events#guild-create
    """

    user_id: Snowflake | None = None
    """User id.

    These field is ommitted on the member sent within each thread in the `GUILD_CREATE` event.
    More info at https://discord.com/developers/docs/topics/gateway-events#guild-create
    """

    join_timestamp: datetime
    """Time the current user last joined the thread."""

    flags: int
    """Any user-thread settings.

    Currently only used for notifications.
    """


class Channel(BaseModel):
    """Channel object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#channel-object-channel-structure
    """

    id: Snowflake
    """Channel id."""

    type: ChannelType

    guild_id: Snowflake | None = None
    """Guild id.

    May be missing for some channel objects received over gateway guild dispatches.
    """

    position: int | None = None
    """Sorting position of the channel"""

    permission_overwrites: list[Overwrite] | None = None
    """Explicit permission overwrites for members and roles."""

    name: str | None = Field(None, min_length=1, max_length=100)
    """Channel name (2-100 characters)"""

    topic: str | None = None
    """Channel topic.

    Should be between 0 and 1024 characters.
    """

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    last_message_id: Snowflake | None = None
    """Last id message sent in this channel.

    May not point to an existing or valid message.
    """

    bitrate: int | None = None
    """Bitrate of the voice channel."""

    user_limit: int | None = None
    """User limit of the voice channel."""

    rate_limit_per_user: int | None = Field(None, min=0, max=21600)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600.

    Bots, as well as users with the permission manage_messages or manage_channel,
    are unaffected. `rate_limit_per_user` also applies to thread creation.
    Users can send one message and create one thread during each
    `rate_limit_per_user` interval.
    """

    recipients: list[User] | None = None
    """Recipients of the DM."""

    icon: str | None = None
    """Icon hash."""

    owner_id: Snowflake | None = None
    """Creator id of the group DM or thread."""

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
    """Camera video quality mode of the voice channel, 1 when not present."""

    message_count: int | None = None
    """Approximate count of messages in a thread, stops counting at 50."""

    member_count: int | None = None
    """Approximate count of users in a thread, stops counting at 50."""

    thread_metadata: ThreadMetadata | None = None
    """Thread-specific fields not needed by other channels."""

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

    @field_validator('topic')
    def validate_topic(cls, topic: str | None, field_info: FieldValidationInfo) -> str | None:
        """Validate topic field."""
        if not topic:
            return topic

        channel_type = field_info.data['type']

        max_guold_text_topic_length = 1024
        max_guild_forum_topic_length = 4096

        if channel_type is ChannelType.GUILD_TEXT and len(topic) > max_guold_text_topic_length:
            raise ValueError('Text channel topic must be between 0 and 1024 characters.')

        if channel_type is ChannelType.GUILD_FORUM and len(topic) > max_guild_forum_topic_length:
            raise ValueError('Forum channel topic must be between 0 and 4096 characters.')

        return topic


class ChannelMention(BaseModel):
    """Channel mention object.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#channel-mention-object
    """

    id: Snowflake
    """Channel id."""

    guild_id: Snowflake
    """Guild id containing the channel."""

    type: ChannelType
    """Channel type."""

    name: str
    """Channel name."""


class ForumTag(BaseModel):
    """Forum tag representation.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#forum-tag-object
    """

    id: Snowflake
    """Tag id."""

    name: str = Field(..., min_length=0, max_length=20)
    """Tag name.

    Should be between 0 and 20 characters.
    """

    moderated: bool
    """Whether this tag can only be used a member with the MANAGE_THREADS permission."""

    emoji_id: Snowflake | None
    """Id of a guild's custom emoji."""

    emoji_name: str | None
    """Unicode character of the emoji."""

    @field_validator('emoji_id')
    def validate_emoji(cls, emoji_id: Snowflake | None, field_info: FieldValidationInfo) -> Snowflake | None:
        """Validate emoji_id and emoji_name fields."""
        if emoji_id is not None and field_info.data['emoji_name'] is not None:
            raise ValueError('emoji_id and emoji_name cannot be set at the same time')
