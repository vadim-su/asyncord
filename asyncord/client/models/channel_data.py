"""This module contains the models for channel data.

Reference: https://discord.com/developers/docs/resources/channel
"""

from __future__ import annotations

import enum
from typing import Any, Literal, Union

from pydantic import BaseModel, Field, model_validator

from asyncord.client.models.channels import ChannelFlag, ChannelType, Overwrite
from asyncord.snowflake import Snowflake

MIN_BITRATE = 8000
"""Minimum bitrate for voice channels."""
MAX_BITRATE = 384000
"""Maximum bitrate for voice channels."""
MAX_RATELIMIT = 21600
"""Maximum ratelimit for channels."""


class ThreadSortOrder(enum.IntEnum):
    """Thread sort order.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-object-sort-order-types
    """

    LATEST_ACTIVITY = 0
    """Sort forum posts by activity."""

    CREATION_DATE = 1
    """Sort forum posts by creation time (from most recent to oldest)."""


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


class ForumTag(BaseModel):
    """An object that represents a tag that is able to be applied to a GUILD_FORUM thread.

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

    emoji_id: Snowflake
    """ID of a guild's custom emoji.

    At most one of emoji_id and emoji_name may be set.
    """

    emoji_name: str
    """Unicode character of the emoji.

    At most one of emoji_id and emoji_name may be set.
    """

    @model_validator(mode='before')
    def validate_emoji_id_or_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate that only one of emoji_id and emoji_name is set."""
        if 'emoji_id' in values and 'emoji_name' in values:
            raise ValueError('At most one of emoji_id and emoji_name may be set.')

        return values


class DefaultReaction(BaseModel):
    """Model specifies the emoji to use as the default way to react to a forum post.

    More info:
    https://discord.com/developers/docs/resources/channel#default-reaction-object
    """

    emoji_id: Snowflake | None = None
    """ID of a guild's custom emoji."""

    emoji_name: str | None = None
    """Unicode character of the emoji."""

    @model_validator(mode='before')
    def validate_emoji_id_or_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate that only one of emoji_id and emoji_name is set."""
        if 'emoji_id' in values and 'emoji_name' in values:
            raise ValueError('At most one of emoji_id and emoji_name may be set.')

        return values


# TODO: #22 Separate into different models
class CreateChannelData(BaseModel):
    """Data to create a channel with.

    This is the data to create a channel with.

    More info at: https://discord.com/developers/docs/resources/guild#create-guild-channel-json-params
    """

    name: str
    """Channel name."""

    type: ChannelType
    """Type of channel."""

    topic: str | None = Field(None, max_length=1024)
    """Channel topic."""

    bitrate: int | None = Field(None, ge=MIN_BITRATE, le=MAX_BITRATE)
    """Bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    Bitrate can be set up to 64000.
    """

    user_limit: int | None = Field(None, ge=0, le=99)
    """User limit of the voice channel.

    0 refers to no limit, 1 to 99 refers to a user limit.
    """

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    position: int | None = None
    """Position of the channel in the left-hand listing"""

    permission_overwrites: list[Overwrite] | None = None
    """Channel or category-specific permissions."""

    parent_id: Snowflake | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rtc_region: str | None = None
    """Channel voice region id of the voice or stage channel.

    Automatic when set to null.
    """

    video_quality_mode: VideoQualityMode | None = None
    """Camera video quality mode of the voice channel."""

    default_auto_archive_duration: Literal[60, 14400, 86400] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """

    default_thread_rate_limit_per_user: int | None = None
    """Initial rate_limit_per_user to set on newly created threads in a channel.

    This field is copied to the thread at creation time and does not live update.
    """

    default_reaction_emoji: DefaultReaction | None = None
    """Emoji to show in the add reaction button on a thread in a GUILD_FORUM channel."""

    available_tags: list[ForumTag] | None = None
    """Set of tags that can be used in a GUILD_FORUM channel."""

    default_sort_order: ThreadSortOrder | None = None
    """Default sort order type used to order posts in GUILD_FORUM channels."""


class UpdatGroupDMChannelData(BaseModel):
    """Model for updating a Group DM Channel.

    Reference:
    https://discord.com/developers/docs/resources/channel#modify-channel-json-params-group-dm
    """

    name: str | None = Field(None, min_length=1, max_length=100)
    """Character channel name."""

    icon: str | None = None
    """Base64 encoded icon"""


class _BaseGuildChannelUpdateData(BaseModel):
    """Base model for updating a Guild Channel."""

    name: str | None = Field(None, min_length=1, max_length=100)
    """Channel name."""

    position: int | None = None
    """position of the channel in the left-hand listing."""

    permission_overwrites: list[Overwrite] | None = None
    """Channel or category-specific permissions."""


class UpdateTextChannelData(_BaseGuildChannelUpdateData):
    """Model for updating a Text Channel.

    Reference:
    https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    type: Literal[ChannelType.GUILD_TEXT] | None = None
    """Type of channel.

    Only conversion between text and announcement is supported and only in guilds
    with the "NEWS" feature.
    """

    topic: str | None = Field(None, max_length=1024)
    """Character channel topic."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: Snowflake | None = None
    """ID of the new parent category for a channel."""

    default_auto_archive_duration: Literal[60, 14400, 86400] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """

    default_thread_rate_limit_per_user: int | None = None
    """Initial rate_limit_per_user to set on newly created threads in a channel.

    This field is copied to the thread at creation time and does not live update.
    """


class UpdateAnnounceChannelData(_BaseGuildChannelUpdateData):
    """Model for updating an Announcement Channel.

    Re
    https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    type: Literal[ChannelType.ANNOUNCEMENT_THREAD] | None = None
    """Type of channel.

    Only conversion between text and announcement is supported and only in guilds
    with the "NEWS" feature.
    """

    topic: str | None = Field(None, max_length=1024)
    """Character channel topic."""

    nsfw: bool | None = None
    """Whether the channel is nsfw/"""

    parent_id: Snowflake | None = None
    """ID of the new parent category for a channel."""

    default_auto_archive_duration: Literal[60, 14400, 86400] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """


class UpdateVoiceChannelData(_BaseGuildChannelUpdateData):
    """Model for updating a Voice Channel.

    Reference:
    https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    bitrate: int | None = Field(None, ge=MIN_BITRATE, le=MAX_BITRATE)
    """Bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    Bitrate can be set up to 64000.
    """

    user_limit: int | None = Field(None, ge=0, le=99)
    """User limit of the voice channel.

    0 refers to no limit, 1 to 99 refers to a user limit.
    """

    parent_id: Snowflake | None = None
    """ID of the new parent category for a channel."""

    rtc_region: Snowflake | None = None
    """Channel voice region id of the voice or stage channel.

    Automatic when set to null.
    """

    video_quality_mode: VideoQualityMode | None = None
    """Camera video quality mode of the voice channel."""


class UpdateStageChannelData(_BaseGuildChannelUpdateData):
    """Model for updating a Stage Channel.

    Reference:
    https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    bitrate: int | None = Field(None, ge=MIN_BITRATE, le=MAX_BITRATE)
    """Bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    Bitrate can be set up to 64000.
    """

    # it possible to be removed because it's not documented
    parent_id: Snowflake | None = None
    """ID of the new parent category for a channel."""

    rtc_region: Snowflake | None = None
    """Channel voice region id of the voice or stage channel, automatic when set to null."""


class UpdateForumChannelData(_BaseGuildChannelUpdateData):
    """Model for updating a Forum Channel.

    Reference:
    https://discord.com/developers/docs/resources/channel#modify-channel-json-params-guild-channel
    """

    topic: str | None = Field(None, max_length=4096)
    """Character channel topic (0-4096 characters)."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: Snowflake | None = None
    """ID of the new parent category for a channel."""

    default_auto_archive_duration: int | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity."""

    flags: Literal[ChannelFlag.NONE, ChannelFlag.REQUIRE_TAG] | None = None
    """Flags of the channel."""

    available_tags: list[ForumTag] | None = None
    """Set of tags that can be used in a GUILD_FORUM channel."""

    default_reaction_emoji: DefaultReaction | None = None
    """Emoji to show in the add reaction button on a thread in a GUILD_FORUM channel."""

    default_thread_rate_limit_per_user: int | None = None
    """Initial rate_limit_per_user to set on newly created threads in a channel.

    This field is copied to the thread at creation time and does not live update.
    """

    default_sort_order: ThreadSortOrder | None = None
    """Default sort order type used to order posts in GUILD_FORUM channels."""


UpdateChannelDataType = Union[  # noqa: UP007
    UpdateTextChannelData,
    UpdateForumChannelData,
    UpdateStageChannelData,
    UpdateVoiceChannelData,
    UpdatGroupDMChannelData,
    UpdateAnnounceChannelData,
]
"""Type of data to update a channel."""
