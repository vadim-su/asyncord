"""Input models for creating channels.

Reference:
https://discord.com/developers/docs/resources/channel
"""

from typing import Any, Literal, Union

from pydantic import BaseModel, Field, model_validator

from asyncord.client.channels.models.common import (
    MAX_BITRATE,
    MAX_RATELIMIT,
    MIN_BITRATE,
    BaseDefaultReaction,
    BaseOverwrite,
    BaseTag,
    ChannelType,
    DefaultForumLayoutType,
    ThreadSortOrder,
    VideoQualityMode,
)
from asyncord.snowflake import SnowflakeInput


class DefaultReactionInput(BaseDefaultReaction):
    """Model specifies the emoji to use as the default way to react to a forum post.

    More info:
    https://discord.com/developers/docs/resources/channel#default-reaction-object
    """

    emoji_id: SnowflakeInput | None = None
    """ID of a guild's custom emoji."""

    @model_validator(mode='before')
    def validate_emoji_id_or_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate that only one of emoji_id and emoji_name is set."""
        if 'emoji_id' in values and 'emoji_name' in values:
            raise ValueError('At most one of emoji_id and emoji_name may be set.')

        return values


class OverwriteInput(BaseOverwrite):
    """Overwrite input object.

    See permissions for more info about `allow` and `deny` fields:
    https://discord.com/developers/docs/topics/permissions#permissions

    Reference:
    https://discord.com/developers/docs/resources/channel#overwrite-object
    """

    id: SnowflakeInput
    """Role or user id."""


class TagInput(BaseTag):
    """Object that represents a tag.

    Can be used in GUILD_FORUM and GUILD_MEDIA channels.

    Reference:
    https://discord.com/developers/docs/resources/channel#forum-tag-object
    """

    id: SnowflakeInput
    """ID of the tag."""

    emoji_id: SnowflakeInput
    """ID of a guild's custom emoji.

    At most one of emoji_id and emoji_name may be set.
    """

    @model_validator(mode='before')
    def validate_emoji_id_or_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate that only one of emoji_id and emoji_name is set."""
        if 'emoji_id' in values and 'emoji_name' in values:
            raise ValueError('At most one of emoji_id and emoji_name may be set.')

        return values


class BaseCreateChannel(BaseModel):
    """Base data to create a channel with."""

    name: str = Field(min_length=1, max_length=100)
    """Channel name."""

    type: ChannelType
    """Type of channel."""

    position: int | None = None
    """Position of the channel in the left-hand listing"""

    permission_overwrites: list[OverwriteInput] | None = None
    """Channel or category-specific permissions."""


class CreateCategoryChannelInput(BaseCreateChannel):
    """Data to create a guild category with."""

    type: Literal[ChannelType.GUILD_CATEGORY] = ChannelType.GUILD_CATEGORY
    """Type of channel."""


class CreateTextChannelInput(BaseCreateChannel):
    """Data to create a text channel with."""

    type: Literal[ChannelType.GUILD_TEXT] = ChannelType.GUILD_TEXT
    """Type of channel."""

    topic: str | None = Field(None, max_length=1024)
    """Channel topic."""

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInput | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """

    default_thread_rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class CreateAnoncementChannelInput(BaseCreateChannel):
    """Data to create an announcement channel with."""

    type: Literal[ChannelType.GUILD_ANNOUNCEMENT] = ChannelType.GUILD_ANNOUNCEMENT
    """Type of channel."""

    topic: str | None = Field(None, max_length=1024)
    """Channel topic."""

    parent_id: SnowflakeInput | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """

    default_thread_rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class CreateForumChannelInput(BaseCreateChannel):
    """Data to create a forum channel with."""

    type: Literal[ChannelType.GUILD_FORUM] = ChannelType.GUILD_FORUM
    """Type of channel."""

    topic: str | None = Field(None, max_length=1024)
    """Channel topic."""

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInput | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    default_reaction_emoji: DefaultReactionInput | None = None
    """Default reaction emoji for the forum channel."""

    available_tags: list[TagInput] | None = None
    """List of available tags for the forum channel."""

    default_sort_order: ThreadSortOrder | None = None
    """Default sort order for the forum channel."""

    default_forum_layout: DefaultForumLayoutType | None = None
    """Default layout for the forum channel."""

    default_thread_rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class CreateMediaChannelInput(BaseCreateChannel):
    """Data to create a media channel with."""

    type: Literal[ChannelType.GUILD_MEDIA] = ChannelType.GUILD_MEDIA
    """Type of channel."""

    topic: str | None = Field(None, max_length=1024)
    """Channel topic."""

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInput | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    default_reaction_emoji: DefaultReactionInput | None = None
    """Default reaction emoji for the media channel."""

    available_tags: list[TagInput] | None = None
    """List of available tags for the media channel."""

    default_thread_rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class CreateVoiceChannelInput(BaseCreateChannel):
    """Data to create a voice channel with."""

    type: Literal[ChannelType.GUILD_VOICE] = ChannelType.GUILD_VOICE
    """Type of channel."""

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

    No limit if set to 0.
    """

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInput | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rtc_region: str | None = None
    """Region for the voice channel.
    
    Automatic when set to None.
    """

    video_quality_mode: VideoQualityMode | None = None
    """Camera video quality mode of the voice channel."""


class CreateStageChannelInput(BaseCreateChannel):
    """Data to create a stage channel with."""

    type: Literal[ChannelType.GUILD_STAGE_VOICE] = ChannelType.GUILD_STAGE_VOICE
    """Type of channel."""

    bitrate: int | None = Field(None, ge=MIN_BITRATE, le=MAX_BITRATE)
    """Bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    """

    user_limit: int | None = Field(None, ge=0, le=99)
    """User limit of the voice channel.

    No limit if set to 0.
    """

    rate_limit_per_user: int | None = Field(None, ge=0, le=MAX_RATELIMIT)
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInput | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rtc_region: str | None = None
    """Region for the voice channel.
    
    Automatic when set to None.
    """

    video_quality_mode: VideoQualityMode | None = None
    """Camera video quality mode of the voice channel."""


type CreateChannelInputType = Union[
    CreateCategoryChannelInput,
    CreateTextChannelInput,
    CreateAnoncementChannelInput,
    CreateForumChannelInput,
    CreateMediaChannelInput,
    CreateVoiceChannelInput,
    CreateStageChannelInput,
]
"""Type of data to create a channel with."""
