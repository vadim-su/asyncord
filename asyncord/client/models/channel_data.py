from __future__ import annotations

import enum
from typing import Union, Literal

from pydantic import Field, BaseModel, root_validator

from asyncord.snowflake import Snowflake
from asyncord.client.models.channels import Overwrite, ChannelFlag, ChannelType

MIN_BITRATE = 8000
MAX_BITRATE = 384000

MAX_RATELIMIT = 21600


class CreateChannelData(BaseModel):
    """Create Channel Data.

    This is the data to create a channel with.

    More info at: https://discord.com/developers/docs/resources/guild#create-guild-channel-json-params
    """

    name: str
    """channel name."""

    type: ChannelType
    """the type of channel."""

    topic: str | None = Field(None, max_length=1024)
    """channel topic."""

    bitrate: int | None = Field(None, ge=MIN_BITRATE, le=MAX_BITRATE)
    """The bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    Bitrate can be set up to 64000.
    """

    user_limit: int | None = Field(None, ge=0, le=99)
    """The user limit of the voice channel.

    0 refers to no limit, 1 to 99 refers to a user limit.
    """

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    position: int | None = None
    """the position of the channel in the left-hand listing"""

    permission_overwrites: list[Overwrite] | None = None
    """channel or category-specific permissions."""

    parent_id: Snowflake | None = None
    """id of the new parent category for a channel"""

    nsfw: bool | None = None
    """whether the channel is nsfw"""

    rtc_region: str | None = None
    """channel voice region id of the voice or stage channel, automatic when set to null."""

    video_quality_mode: VideoQualityMode | None = None
    """the camera video quality mode of the voice channel."""

    default_auto_archive_duration: Literal[60, 14400, 86400] | None = None
    """the default duration that the clients use (not the API) for
    newly created threads in the channel, in minutes, to automatically archive
    the thread after recent activity.
    """

    default_reaction_emoji: DefaultReaction | None = None
    """the emoji to show in the add reaction button on a thread in a GUILD_FORUM channel"""

    available_tags: list[ForumTag] | None = None
    """the set of tags that can be used in a GUILD_FORUM channel"""

    default_sort_order: ThreadSortOrder | None = None
    """the default sort order type used to order posts in GUILD_FORUM channels"""


class UpdatGroupDMChannelData(BaseModel):
    """https: // discord.com / developers / docs / resources / channel  # modify-channel-json-params-group-dm"""
    name: str | None = Field(None, min_length=1, max_length=100)
    """character channel name."""

    icon: str | None = None
    """base64 encoded icon"""


class _BaseGuildChannelUpdateData(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    """channel name."""

    position: int | None = None
    """the position of the channel in the left-hand listing"""

    permission_overwrites: list[Overwrite] | None = None
    """channel or category-specific permissions."""


class UpdateTextChannelData(_BaseGuildChannelUpdateData):
    """https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel"""

    type: Literal[ChannelType.GUILD_TEXT] | None = None
    """Type of channel.

    Only conversion between text and announcement is supported and only in guilds
    with the "NEWS" feature.
    """

    topic: str | None = Field(None, max_length=1024)
    """character channel topic"""

    nsfw: bool | None = None
    """whether the channel is nsfw"""

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: Snowflake | None = None
    """id of the new parent category for a channel"""

    default_auto_archive_duration: Literal[60, 14400, 86400] | None = None
    """the default duration that the clients use (not the API) for
    newly created threads in the channel, in minutes, to automatically archive
    the thread after recent activity"""

    default_thread_rate_limit_per_user: int | None = None
    """the initial rate_limit_per_user to set on newly created threads in a channel.

    This field is copied to the thread at creation time and does not live update.
    """


class UpdateAnnounceChannelData(UpdateTextChannelData):
    """https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel"""

    type: Literal[ChannelType.ANNOUNCEMENT_THREAD] | None = None
    """Type of channel.

    Only conversion between text and announcement is supported and only in guilds
    with the "NEWS" feature.
    """

    topic: str | None = Field(None, max_length=1024)
    """character channel topic"""

    nsfw: bool | None = None
    """whether the channel is nsfw"""

    parent_id: Snowflake | None = None
    """id of the new parent category for a channel"""

    default_auto_archive_duration: Literal[60, 14400, 86400] | None = None
    """the default duration that the clients use (not the API) for
    newly created threads in the channel, in minutes, to automatically archive
    the thread after recent activity.
    """


class UpdateVoiceChannelData(_BaseGuildChannelUpdateData):
    """https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel"""

    bitrate: int | None = Field(None, ge=MIN_BITRATE, le=MAX_BITRATE)
    """The bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    Bitrate can be set up to 64000.
    """

    user_limit: int | None = Field(None, ge=0, le=99)
    """The user limit of the voice channel.

    0 refers to no limit, 1 to 99 refers to a user limit.
    """

    parent_id: Snowflake | None = None
    """id of the new parent category for a channel"""

    rtc_region: Snowflake | None = None
    """channel voice region id of the voice or stage channel, automatic when set to null."""

    video_quality_mode: VideoQualityMode | None = None
    """the camera video quality mode of the voice channel."""


class UpdateStageChannelData(_BaseGuildChannelUpdateData):
    """https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel"""

    bitrate: int | None = Field(None, ge=MIN_BITRATE, le=MAX_BITRATE)
    """The bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    Bitrate can be set up to 64000.
    """

    # it possible to be removed because it's not documented
    parent_id: Snowflake | None = None
    """id of the new parent category for a channel"""

    rtc_region: Snowflake | None = None
    """channel voice region id of the voice or stage channel, automatic when set to null."""


class UpdateForumChannelData(_BaseGuildChannelUpdateData):
    """https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel"""

    topic: str | None = Field(None, max_length=4096)
    """character channel topic (0-4096 characters)"""

    nsfw: bool | None = None
    """whether the channel is nsfw"""

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: Snowflake | None = None
    """id of the new parent category for a channel"""

    default_auto_archive_duration: int | None = None
    """the default duration that the clients use (not the API) for
    newly created threads in the channel, in minutes, to automatically archive
    the thread after recent activity"""

    flags: Literal[ChannelFlag.NONE, ChannelFlag.REQUIRE_TAG] | None = None

    available_tags: list[ForumTag] | None = None
    """the set of tags that can be used in a GUILD_FORUM channel"""

    default_reaction_emoji: DefaultReaction | None = None
    """the emoji to show in the add reaction button on a thread in a GUILD_FORUM channel"""

    default_thread_rate_limit_per_user: int | None = None
    """the initial rate_limit_per_user to set on newly created threads in a channel.

    This field is copied to the thread at creation time and does not live update.
    """

    default_sort_order: ThreadSortOrder | None = None
    """the default sort order type used to order posts in GUILD_FORUM channels"""


UpdateChannelDataType = Union[
    UpdateTextChannelData,
    UpdateForumChannelData,
    UpdateStageChannelData,
    UpdateVoiceChannelData,
    UpdatGroupDMChannelData,
    UpdateAnnounceChannelData,
]


@enum.unique
class VideoQualityMode(enum.IntEnum):
    """https://discord.com/developers/docs/resources/channel#channel-object-video-quality-modes"""

    AUTO = 1
    """Discord chooses the quality for optimal performance."""

    FULL = 2
    """720p"""


class ForumTag(BaseModel):
    """An object that represents a tag that is able to be applied to a thread in
    a GUILD_FORUM channel.

    https://discord.com/developers/docs/resources/channel#forum-tag-object
    """

    id: Snowflake
    """the id of the tag"""

    name: str
    """the name of the tag (0-20 characters)"""

    moderated: bool
    """Whether this tag can only be added to or removed from threads by a member
    with the MANAGE_THREADS permission"""

    emoji_id: Snowflake
    """the id of a guild's custom emoji

    At most one of emoji_id and emoji_name may be set.
    """

    emoji_name: str
    """the unicode character of the emoji

    At most one of emoji_id and emoji_name may be set.
    """

    @root_validator
    def check_emoji_id_or_name(cls, values):
        if 'emoji_id' in values and 'emoji_name' in values:
            raise ValueError('At most one of emoji_id and emoji_name may be set.')

        return values


class DefaultReaction(BaseModel):
    """An object that specifies the emoji to use as the default way to react to a forum post.

    More info:
    https://discord.com/developers/docs/resources/channel#default-reaction-object"""

    emoji_id: Snowflake | None = None
    """the id of a guild's custom emoji"""

    emoji_name: str | None = None
    """the unicode character of the emoji"""

    @root_validator
    def check_emoji_id_or_emoji_name(cls, values):
        if 'emoji_id' in values and 'emoji_name' in values:
            raise ValueError('At most one of emoji_id and emoji_name may be set.')

        return values


class ThreadSortOrder(enum.IntEnum):
    """https://discord.com/developers/docs/resources/channel#channel-object-sort-order-types"""

    LATEST_ACTIVITY = 0
    """Sort forum posts by activity"""

    CREATION_DATE = 1
    """Sort forum posts by creation time (from most recent to oldest)"""
