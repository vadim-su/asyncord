"""Channel update models.

Reference:
https://discord.com/developers/docs/resources/channel
"""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, ValidationInfo, field_serializer, field_validator

from asyncord.base64_image import Base64ImageInputType
from asyncord.client.channels.models.common import (
    MAX_BITRATE,
    MAX_RATELIMIT,
    MIN_BITRATE,
    ChannelFlag,
    ChannelType,
    DefaultForumLayoutType,
    ThreadSortOrder,
    VideoQualityMode,
)
from asyncord.client.channels.models.requests.creation import (
    DefaultReaction,
    Overwrite,
    Tag,
)
from asyncord.client.models.permissions import PermissionFlag
from asyncord.snowflake import SnowflakeInputType

__all__ = (
    'BaseUpdateChannel',
    'UpdateAnnouncementChannelRequest',
    'UpdateChannelPermissionsRequest',
    'UpdateChannelPositionRequest',
    'UpdateChannelRequest',
    'UpdateChannelRequestType',
    'UpdateForumChannelRequest',
    'UpdateGroupDMChannelRequest',
    'UpdateGuildCategoryRequest',
    'UpdateMediaChannelRequest',
    'UpdateStageChannelReuqest',
    'UpdateTextChannelRequest',
    'UpdateVoiceChannelRequest',
)


class BaseUpdateChannel(BaseModel):
    """Data to create a channel with."""

    name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    """Channel name."""

    position: int | None = None
    """Position of the channel in the left-hand listing"""

    permission_overwrites: list[Overwrite] | None = None
    """Channel or category-specific permissions."""


class UpdateGuildCategoryRequest(BaseUpdateChannel):
    """Data to update a guild category with."""


class UpdateChannelRequest(BaseUpdateChannel):
    """Data to update a channel with.

    If you don't know the type of channel you're updating, use this.
    Can't update DM channels.
    """

    type: Literal[ChannelType.GUILD_TEXT, ChannelType.GUILD_ANNOUNCEMENT] | None = None
    """Type of channel.

    Only conversion between text and announcement is supported and only in guilds
    with the "NEWS" feature.
    """

    topic: Annotated[str, Field(max_length=1024)] | None = None
    """Character channel topic."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rate_limit_per_user: Annotated[int, Field(ge=0, le=MAX_RATELIMIT)] | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    bitrate: Annotated[int, Field(ge=MIN_BITRATE, le=MAX_BITRATE)] | None = None
    """Bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    """

    user_limit: Annotated[int, Field(ge=0, le=99)] | None = None
    """User limit of the voice channel.

    No limit if set to 0.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    rtc_region: str | None = None
    """Region for the voice channel.

    Automatic when set to None.
    """

    video_quality_mode: VideoQualityMode | None = None
    """Camera video quality mode of the voice channel."""

    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """

    flags: ChannelFlag | None = None
    """Channel flags."""

    available_tags: list[Tag] | None = None
    """List of available tags for the channel."""

    default_reaction_emoji: DefaultReaction | None = None
    """Default reaction emoji for the forum channel."""

    default_thread_rate_limit_per_user: Annotated[int, Field(ge=0, le=MAX_RATELIMIT)] | None = None
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    default_sort_order: ThreadSortOrder | None = None
    """Default sort order for the forum channel."""

    default_forum_layout: DefaultForumLayoutType | None = None
    """Default layout for the forum channel."""

    applied_tags: list[SnowflakeInputType] | None = None
    """Set of tag ids that have been applied to a thread."""

    @field_validator('flags')
    @classmethod
    def validate_flags(cls, flags: ChannelFlag | None, field_info: ValidationInfo) -> ChannelFlag | None:
        """Validate flags."""
        if not flags:
            return flags

        channel_type: ChannelType | None = field_info.data.get('type')

        # I know channel_type can't be GUILD_FORUM and GUILD_MEDIA. It's for logic consistency.
        if flags and channel_type not in {ChannelType.GUILD_FORUM, ChannelType.GUILD_MEDIA}:
            raise ValueError('Flags can only be set for forum and media channels')

        return flags


class UpdateGroupDMChannelRequest(BaseModel):
    """Data to update a group DM channel with.

    Reference:
    https://discord.com/developers/docs/resources/channel#modify-channel-json-params-group-dm
    """

    name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    """Character channel name."""

    icon: Base64ImageInputType | None = None
    """Base64 encoded icon"""


class UpdateTextChannelRequest(BaseUpdateChannel):
    """Data to update a text channel with."""

    type: Literal[ChannelType.GUILD_TEXT] | None = None
    """Type of channel."""

    topic: str | None = None
    """Channel topic."""

    rate_limit_per_user: int | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """

    default_thread_rate_limit_per_user: Annotated[int, Field(ge=0, le=MAX_RATELIMIT)] | None = None
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class UpdateAnnouncementChannelRequest(BaseUpdateChannel):
    """Data to update an announcement channel with."""

    type: Literal[ChannelType.GUILD_ANNOUNCEMENT] | None = None
    """Type of channel."""

    topic: str | None = None
    """Channel topic."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """


class UpdateForumChannelRequest(BaseUpdateChannel):
    """Data to update a forum channel with."""

    topic: str | None = None
    """Channel topic."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rate_limit_per_user: int | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    flags: ChannelFlag | None = None
    """Channel flags."""

    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """This field represents the default duration in minutes.

    That clients use to automatically archive newly created threads in the channel
    after recent activity.
    """

    @field_validator('flags')
    @classmethod
    def validate_flags(cls, flags: ChannelFlag | None, field_info: ValidationInfo) -> ChannelFlag | None:
        """Validate flags."""
        if flags and ChannelFlag.HIDE_MEDIA_DOWNLOAD_OPTIONS in flags:
            raise ValueError('HIDE_MEDIA_DOWNLOAD_OPTIONS flag can only be set for media channels')

        return flags


class UpdateMediaChannelRequest(BaseUpdateChannel):
    """Data to update a media channel with."""

    topic: str | None = None
    """Channel topic."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rate_limit_per_user: int | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    flags: ChannelFlag | None = None
    """Channel flags."""

    available_tags: list[Tag] | None = None
    """List of available tags for the channel."""

    default_reaction_emoji: DefaultReaction | None = None
    """Default reaction emoji for the forum channel."""

    default_thread_rate_limit_per_user: Annotated[int, Field(ge=0, le=MAX_RATELIMIT)] | None = None
    """Amount of seconds a user has to wait before sending another message in a thread.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """


class UpdateVoiceChannelRequest(BaseUpdateChannel):
    """Data to update a voice channel with."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rate_limit_per_user: int | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600. Bots, as well as users with the permission
    manage_messages or manage_channel, are unaffected.
    """

    bitrate: int | None = None
    """Bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    """

    user_limit: int | None = None
    """User limit of the voice channel.

    No limit if set to 0.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    rtc_region: str | None = None
    """Region for the voice channel.

    Automatic when set to None.
    """

    video_quality_mode: VideoQualityMode | None = None
    """Camera video quality mode of the voice channel."""


class UpdateStageChannelReuqest(BaseUpdateChannel):
    """Data to update a stage channel with."""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    bitrate: int | None = None
    """Bitrate (in bits) of the voice channel.

    For voice channels, normal servers can set bitrate up to 96000.
    Servers with Boost level 1 can set up to 128000, servers with Boost level 2
    can set up to 256000, and servers with Boost level 3 or the VIP_REGIONS guild
    feature can set up to 384000. For stage channels.
    """

    user_limit: int | None = None
    """User limit of the voice channel.

    No limit if set to 0.
    """

    parent_id: SnowflakeInputType | None = None
    """ID of the new parent category for a channel."""

    rtc_region: str | None = None
    """Region for the voice channel.

    Automatic when set to None.
    """

    video_quality_mode: VideoQualityMode | None = None
    """Camera video quality mode of the voice channel."""


class UpdateChannelPermissionsRequest(BaseModel):
    """Data to update a channel's permissions with.

    Reference:
    https://discord.com/developers/docs/resources/channel#edit-channel-permissions
    """

    type: Literal['role', 'member']
    """Type of the permission overwrite."""

    allow: PermissionFlag | None = None
    """The bitwise value of all allowed permissions.

    Default to None.

    If None, the value will be set 0 at discord's end.
    """

    deny: PermissionFlag | None = None
    """The bitwise value of all disallowed permissions.

    Default to None.

    If None, the value will be set 0 at discord's end.
    """

    @field_serializer('type', when_used='json')
    @classmethod
    def serialize_type(cls, type_value: Literal['role', 'member']) -> int:
        """Serialize type to number for JSON.

        0 if role, 1 if member.
        """
        return int(type_value == 'member')


class UpdateChannelPositionRequest(BaseModel):
    """Data to update a channel's position with.

    Reference:
    https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions-json-params
    """

    id: SnowflakeInputType
    """Channel id."""

    position: int | None = None
    """Position of the channel in the left-hand listing."""

    lock_permissions: bool | None = None
    """Syncs the permission overwrites with the new parent.

    If moving to a new category.
    """

    parent_id: SnowflakeInputType | None = None
    """New parent ID for the channel that is moved."""


type UpdateChannelRequestType = (
    UpdateGuildCategoryRequest
    | UpdateChannelRequest
    | UpdateGroupDMChannelRequest
    | UpdateTextChannelRequest
    | UpdateAnnouncementChannelRequest
    | UpdateForumChannelRequest
    | UpdateMediaChannelRequest
    | UpdateVoiceChannelRequest
    | UpdateStageChannelReuqest
)
"""Type of data to update a channel with."""
