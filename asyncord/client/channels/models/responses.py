"""Channel response models.

Reference:
https://discord.com/developers/docs/resources/channel
"""

from __future__ import annotations

import datetime

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel

from asyncord.client.channels.models.common import (
    ChannelFlag,
    ChannelType,
    DefaultForumLayoutType,
    OverwriteType,
    ThreadSortOrder,
    VideoQualityMode,
)
from asyncord.client.members.models.responses import MemberResponse
from asyncord.client.models.permissions import PermissionFlag
from asyncord.client.users.models.responses import UserResponse
from asyncord.snowflake import Snowflake

__all__ = (
    'ChannelResponse',
    'DefaultReactionOut',
    'FollowedChannelResponse',
    'OverwriteOut',
    'TagOut',
    'ThreadMemberResponse',
)


class OverwriteOut(BaseModel):
    """Base overwrite object.

    See permissions for more info about `allow` and `deny` fields:
    https://discord.com/developers/docs/topics/permissions#permissions

    Reference:
    https://discord.com/developers/docs/resources/channel#overwrite-object
    """

    id: Snowflake
    """Role or user id.

    Set corresponding type field.
    """

    type: FallbackAdapter[OverwriteType]
    """Type of overwrite."""

    allow: PermissionFlag
    """Permission flags to allow."""

    deny: PermissionFlag
    """Permission flags to deny."""


class DefaultReactionOut(BaseModel):
    """Model specifies the emoji to use as the default way to react to a forum post.

    Reference:
    https://discord.com/developers/docs/resources/channel#default-reaction-object
    """

    emoji_id: Snowflake | None = None
    """ID of a guild's custom emoji."""

    emoji_name: str | None = None
    """Unicode character of the emoji."""


class TagOut(BaseModel):
    """Object that represents a tag.

    Can be used in GUILD_FORUM and GUILD_MEDIA channels.

    Reference:
    https://discord.com/developers/docs/resources/channel#forum-tag-object
    """

    id: Snowflake
    """ID of the tag."""

    name: str
    """Name of the tag (0-20 characters)."""

    moderated: bool
    """Tag can only be added to or removed from threads.

    It allowed only for members with the MANAGE_THREADS permission.
    """

    emoji_id: Snowflake | None = None
    """ID of a guild's custom emoji.

    At most one of emoji_id and emoji_name may be set.
    """

    emoji_name: str | None = None
    """Unicode character of the emoji.

    At most one of emoji_id and emoji_name may be set.
    """


class ThreadMemberResponse(BaseModel):
    """Thread member object.

    Reference:
    https://discord.com/developers/docs/resources/channel#thread-member-object
    """

    id: Snowflake | None = None
    """Thread id.

    These field is ommitted on the member sent within each thread in the `GUILD_CREATE` event.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-create
    """

    user_id: Snowflake | None = None
    """User id.

    These field is ommitted on the member sent within each thread in the `GUILD_CREATE` event.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-create
    """

    join_timestamp: datetime.datetime
    """Time the current user last joined the thread."""

    flags: int
    """Any user-thread settings.

    Currently only used for notifications.
    """

    member: MemberResponse | None = None
    """Additional information about the user

    The member field is only present when with_member is set to true
    when calling List Thread Members or Get Thread Member.
    """


class ChannelResponse(BaseModel):
    """Channel object.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-object-channel-structure
    """

    id: Snowflake
    """Channel id."""

    type: FallbackAdapter[ChannelType]
    """Type of channel."""

    guild_id: Snowflake | None = None
    """Guild id.

    May be missing for some channel objects received over gateway guild dispatches.
    """

    position: int | None = None
    """Sorting position of the channel"""

    permission_overwrites: list[OverwriteOut] | None = None
    """Explicit permission overwrites for members and roles."""

    name: str | None = None
    """Channel name (1-100 characters)"""

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

    rate_limit_per_user: int | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600.

    Bots, as well as users with the permission manage_messages or manage_channel,
    are unaffected. `rate_limit_per_user` also applies to thread creation.
    Users can send one message and create one thread during each
    `rate_limit_per_user` interval.
    """

    recipients: list[UserResponse] | None = None
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

    last_pin_timestamp: datetime.datetime | None = None
    """Timestamp when the last pinned message was pinned.

    This may be null in events such as GUILD_CREATE when a message is not pinned.
    """

    rtc_region: str | None = None
    """Voice region id for the voice channel, automatic when set to null."""

    video_quality_mode: FallbackAdapter[VideoQualityMode] | None = None
    """Camera video quality mode of the voice channel, 1 when not present."""

    default_auto_archive_duration: int | None = None
    """Default duration that the clients (not the API) will use for newly created threads.

    To automatically archive the thread after recent activity.
    Can be set to: 60, 1440, 4320, 10080 minutes (1 hour, 1 day, 3 days, 1 week).
    """

    permissions: str | None = None
    """Computed permissions for the invoking user in the channel, including overwrites.

    Only included when part of the resolved data received
    on a slash command interaction. This does not include implicit permissions,
    which may need to be checked separately
    """

    flags: ChannelFlag | None = None
    """Flags for the channel."""

    available_tags: list[TagOut] | None = None
    """Set of tags that can be used."""

    default_reaction_emoji: DefaultReactionOut | None = None
    """Emoji to show in the add reaction button on a thread."""

    default_thread_rate_limit_per_user: int | None = None
    """Initial rate_limit_per_user to set on newly created threads in a channel.

    This field is copied to the thread at creation time and does not live update.
    """

    default_sort_order: FallbackAdapter[ThreadSortOrder] | None = None
    """Default sort order type used to order posts in GUILD_FORUM channels.

    Defaults to null, which indicates a preferred sort order hasn't been set by a channel admin
    """

    default_forum_layout: FallbackAdapter[DefaultForumLayoutType] | None = None
    """Default forum layout view used to display posts in GUILD_FORUM channels.

    Defaults to 0, which indicates a layout view has not been set by a channel admin.
    """


class FollowedChannelResponse(BaseModel):
    """Followed channel object.

    Reference:
    https://discord.com/developers/docs/resources/channel#followed-channel-object-followed-channel-structure
    """

    channel_id: Snowflake
    """Source channel id."""

    webhook_id: Snowflake
    """Created webhook id."""
