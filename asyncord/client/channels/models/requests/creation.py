"""Input models for creating channels.

Reference:
https://discord.com/developers/docs/resources/channel
"""

import logging
from typing import Annotated, Any, Literal, Self

from pydantic import BaseModel, Field, model_validator

from asyncord.client.channels.models.common import (
    MAX_BITRATE,
    MAX_RATELIMIT,
    MIN_BITRATE,
    ChannelType,
    DefaultForumLayoutType,
    ThreadSortOrder,
    VideoQualityMode,
)
from asyncord.client.guilds.models.common import InviteTargetType
from asyncord.snowflake import SnowflakeInputType

__all__ = (
    'BaseCreateChannel',
    'ChannelInviteRequest',
    'CreateAnoncementChannelRequest',
    'CreateCategoryChannelRequest',
    'CreateChannelRequestType',
    'CreateForumChannelRequest',
    'CreateMediaChannelRequest',
    'CreateStageChannelRequest',
    'CreateTextChannelRequest',
    'CreateVoiceChannelRequest',
    'DefaultReaction',
    'Overwrite',
    'Tag',
)

logger = logging.getLogger(__name__)


class DefaultReaction(BaseModel):
    """Model specifies the emoji to use as the default way to react to a forum post.

    More info:
    https://discord.com/developers/docs/resources/channel#default-reaction-object
    """

    emoji_id: SnowflakeInputType | None = None
    """ID of a guild's custom emoji."""

    emoji_name: str | None = None
    """Unicode character of the emoji."""

    @model_validator(mode='before')
    def validate_emoji_id_or_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate that only one of emoji_id and emoji_name is set."""
        if 'emoji_id' in values and 'emoji_name' in values:
            raise ValueError('At most one of emoji_id and emoji_name may be set.')

        return values


class Overwrite(BaseModel):
    """Overwrite input object.

    See permissions for more info about `allow` and `deny` fields:
    https://discord.com/developers/docs/topics/permissions#permissions

    Reference:
    https://discord.com/developers/docs/resources/channel#overwrite-object
    """

    id: SnowflakeInputType
    """Role or user id."""


class Tag(BaseModel):
    """Object that represents a tag.

    Can be used in GUILD_FORUM and GUILD_MEDIA channels.

    Reference:
    https://discord.com/developers/docs/resources/channel#forum-tag-object
    """

    name: str
    """Name of the tag (0-20 characters)."""

    moderated: bool = False
    """Tag can be added to or removed from threads by a member with the MANAGE_THREADS permission."""

    emoji_id: SnowflakeInputType | None = None
    """ID of a guild's custom emoji.

    At most one of emoji_id and emoji_name may be set.
    """

    emoji_name: str | None = None
    """Unicode character of the emoji.

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

    permission_overwrites: list[Overwrite] | None = None
    """Channel or category-specific permissions."""


class CreateCategoryChannelRequest(BaseCreateChannel):
    """Data to create a guild category with."""

    type: Literal[ChannelType.GUILD_CATEGORY] = ChannelType.GUILD_CATEGORY  # type: ignore
    """Type of channel."""


class CreateTextChannelRequest(BaseCreateChannel):
    """Data to create a text channel with."""

    type: Literal[ChannelType.GUILD_TEXT] = ChannelType.GUILD_TEXT  # type: ignore
    """Type of channel."""

    topic: Annotated[str | None, Field(max_length=1024)] = None
    """Channel topic."""

    rate_limit_per_user: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """

    default_thread_rate_limit_per_user: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class CreateAnoncementChannelRequest(BaseCreateChannel):
    """Data to create an announcement channel with."""

    type: Literal[ChannelType.GUILD_ANNOUNCEMENT] = ChannelType.GUILD_ANNOUNCEMENT  # type: ignore
    """Type of channel."""

    topic: Annotated[str | None, Field(max_length=1024)] = None
    """Channel topic."""

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """

    default_thread_rate_limit_per_user: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class CreateForumChannelRequest(BaseCreateChannel):
    """Data to create a forum channel with."""

    type: Literal[ChannelType.GUILD_FORUM] = ChannelType.GUILD_FORUM  # type: ignore
    """Type of channel."""

    topic: Annotated[str | None, Field(max_length=1024)] = None
    """Channel topic."""

    rate_limit_per_user: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    default_reaction_emoji: DefaultReaction | None = None
    """Default reaction emoji for the forum channel."""

    available_tags: list[Tag] | None = None
    """List of available tags for the forum channel."""

    default_sort_order: ThreadSortOrder | None = None
    """Default sort order for the forum channel."""

    default_forum_layout: DefaultForumLayoutType | None = None
    """Default layout for the forum channel."""

    default_thread_rate_limit_per_user: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class CreateMediaChannelRequest(BaseCreateChannel):
    """Data to create a media channel with."""

    type: Literal[ChannelType.GUILD_MEDIA] = ChannelType.GUILD_MEDIA  # type: ignore
    """Type of channel."""

    topic: Annotated[str | None, Field(max_length=1024)] = None
    """Channel topic."""

    rate_limit_per_user: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    default_reaction_emoji: DefaultReaction | None = None
    """Default reaction emoji for the media channel."""

    available_tags: list[Tag] | None = None
    """List of available tags for the media channel."""

    default_thread_rate_limit_per_user: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class CreateVoiceChannelRequest(BaseCreateChannel):
    """Data to create a voice channel with."""

    type: Literal[ChannelType.GUILD_VOICE] = ChannelType.GUILD_VOICE  # type: ignore
    """Type of channel."""

    bitrate: Annotated[int | None, Field(ge=MIN_BITRATE, le=MAX_BITRATE)] = None
    """Bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    Bitrate can be set up to 64000.
    """

    user_limit: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """User limit of the voice channel.

    No limit if set to 0.
    """

    rate_limit_per_user: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rtc_region: str | None = None
    """Region for the voice channel.

    Automatic when set to None.
    """

    video_quality_mode: VideoQualityMode | None = None
    """Camera video quality mode of the voice channel."""


class CreateStageChannelRequest(BaseCreateChannel):
    """Data to create a stage channel with."""

    type: Literal[ChannelType.GUILD_STAGE_VOICE] = ChannelType.GUILD_STAGE_VOICE  # type: ignore
    """Type of channel."""

    bitrate: Annotated[int | None, Field(ge=MIN_BITRATE, le=MAX_BITRATE)] = None
    """Bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    """

    user_limit: Annotated[int | None, Field(ge=0, le=99)] = None
    """User limit of the voice channel.

    No limit if set to 0.
    """

    rate_limit_per_user: Annotated[int | None, Field(ge=0, le=MAX_RATELIMIT)] = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rtc_region: str | None = None
    """Region for the voice channel.

    Automatic when set to None.
    """

    video_quality_mode: VideoQualityMode | None = None
    """Camera video quality mode of the voice channel."""


class ChannelInviteRequest(BaseModel):
    """Data to create channel invite.

    Reference:
    https://discord.com/developers/docs/resources/channel#create-channel-invite-json-params
    """

    max_age: Annotated[int | None, Field(le=604800)] = None
    """Duration of invite in seconds before expiry, or 0 for never."""

    max_uses: Annotated[int | None, Field(ge=0, le=100)] = None
    """Max number of uses or 0 for unlimited."""

    temporary: bool | None = None
    """Whether this invite only grants temporary membership."""

    unique: bool | None = None
    """If true, don't try to reuse a similar invite.

    Useful for creating many unique one time use invites.
    """

    target_type: InviteTargetType | None = None
    """The type of a target for this voic channel invite."""

    target_user_id: SnowflakeInputType | None = None
    """Id of the user whose stream to display for this invite.

    Required if target_type is `InviteTargetType.STREAM`.
    """

    target_application_id: SnowflakeInputType | None = None
    """Id of the embedded application to open for this invite.

    Required if target_type is `InviteTargetType.EMBEDDED_APPLICATION`.
    """

    @model_validator(mode='after')
    def validate_target_type(self) -> Self:
        """If target_type is set.

        Then target_user_id and target_application_id must be set accordingly.
        """
        match self.target_type:
            case InviteTargetType.STREAM:
                if not self.target_user_id:
                    raise ValueError('target_user_id must be set if target_type is STREAM')

            case InviteTargetType.EMBEDDED_APPLICATION:
                if not self.target_application_id:
                    raise ValueError('target_application_id must be set if target_type is EMBEDDED_APPLICATION')

            case _:
                logger.warning('target_type possibly is not processed.')

        return self


type CreateChannelRequestType = (
    CreateCategoryChannelRequest
    | CreateTextChannelRequest
    | CreateAnoncementChannelRequest
    | CreateForumChannelRequest
    | CreateMediaChannelRequest
    | CreateVoiceChannelRequest
    | CreateStageChannelRequest
)
"""Type of data to create a channel with."""
