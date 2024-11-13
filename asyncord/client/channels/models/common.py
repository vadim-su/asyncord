"""Common channel models for Discord API.

Reference:
https://discord.com/developers/docs/resources/channel
"""

import enum

MIN_BITRATE = 8000
"""Minimum bitrate for voice channels."""
MAX_BITRATE = 384000
"""Maximum bitrate for voice channels."""
MAX_RATELIMIT = 21600
"""Maximum ratelimit for channels."""


@enum.unique
class OverwriteType(enum.IntEnum):
    """Type of overwrite."""

    ROLE = 0
    USER = 1


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

    GUILD_MEDIA = 16
    """Channel that can only contain threads, similar to GUILD_FORUM channels."""


@enum.unique
class ChannelFlag(enum.IntFlag):
    """Channel flags.

    Read more info at:
    https://discord.com/developers/docs/resources/channel#channel-object-channel-flags
    """

    PINNED = 1 << 1
    """Whether the channel is pinned."""

    REQUIRE_TAG = 1 << 4
    """Whether a tag is requiredin a GUILD_FORUM channel.

    Tags are specified in the applied_tags field.
    """

    HIDE_MEDIA_DOWNLOAD_OPTIONS = 1 << 15
    """	When set hides the embedded media download options.
    Available only for media channels
    """


class ThreadSortOrder(enum.IntEnum):
    """Thread sort order.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-object-sort-order-types
    """

    LATEST_ACTIVITY = 0
    """Sort forum posts by activity."""

    CREATION_DATE = 1
    """Sort forum posts by creation time (from most recent to oldest)."""


class DefaultForumLayoutType(enum.IntEnum):
    """Default forum layout type.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-object-forum-layout-types
    """

    NOT_SET = 0
    """No default has been set for forum channel"""

    LIST_VIEW = 1
    """Display posts as a list"""

    GALLERY_VIEW = 2
    """Display posts as a collection of tiles"""


@enum.unique
class VideoQualityMode(enum.IntEnum):
    """Camera video quality modes.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-object-video-quality-modes
    """

    AUTO = 1
    """Discord chooses the quality for optimal performance."""

    FULL = 2
    """720p."""
