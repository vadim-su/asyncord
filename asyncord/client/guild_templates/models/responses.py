"""Models for guild template responses."""

from datetime import datetime

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel

from asyncord.client.channels.models.common import (
    ChannelFlag,
    ChannelType,
)
from asyncord.client.channels.models.responses import OverwriteOut
from asyncord.client.models.permissions import PermissionFlag
from asyncord.client.users.models.responses import UserResponse
from asyncord.color import Color
from asyncord.snowflake import Snowflake

__all__ = (
    'ChannelGuildTemplateOut',
    'GuildGuildTemplateOut',
    'GuildTemplateResponse',
    'RoleGuildTemplateOut',
)


class RoleGuildTemplateOut(BaseModel):
    """Partial role object for guild template response.

    Reference:
    https://discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
    """

    id: Snowflake
    """Role id."""

    name: str
    """Role name."""

    permissions: PermissionFlag
    """Permission bit set"""

    color: Color
    """Integer representation of hexadecimal color code."""

    hoist: bool
    """Whether this role is pinned in the user listing."""

    mentionable: bool
    """Whether this role is mentionable."""


class ChannelGuildTemplateOut(BaseModel):
    """Partial channel object for guild template response.

    Reference:
    https://discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
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

    rtc_region: str | None = None
    """Voice region id for the voice channel, automatic when set to null."""

    permissions: str | None = None
    """Computed permissions for the invoking user in the channel, including overwrites.

    Only included when part of the resolved data received
    on a slash command interaction. This does not include implicit permissions,
    which may need to be checked separately
    """

    flags: ChannelFlag | None = None
    """Flags for the channel."""


class GuildGuildTemplateOut(BaseModel):
    """Partial guild object for guild template response.

    Reference:
    https://discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
    """

    name: str
    """Guild name.

    Should be between 2 and 100 characters excluding trailing and leading whitespace.
    """

    description: str | None
    """Guild description (0-1000 characters)."""

    region: str | None = None
    """Voice region ID for the guild (deprecated)."""

    verification_level: int
    """Verification level required for the guild."""

    default_message_notifications: int
    """Default message notifications level."""

    explicit_content_filter: int
    """Explicit content filter level."""

    preferred_locale: str
    """Preferred locale of a Community guild used in server discovery and notices

    Sent in interactions. Defaults to "en-US".
    """

    afk_timeout: int
    """AFK timeout in seconds."""

    roles: list[RoleGuildTemplateOut] | None = None
    """Roles in the guild."""

    # Doesn't exists in the whole GuildResponse model.
    channels: list[ChannelGuildTemplateOut] | None = None
    """Channels in the guild."""

    afk_channel_id: Snowflake | None = None
    """ID of AFK channel."""

    system_channel_id: Snowflake | None
    """ID of the channel where guild notices such as welcome messages and boost events are posted."""

    system_channel_flags: int
    """System channel flags."""

    icon_hash: str | None = None
    """Icon hash, returned when in the template object."""


class GuildTemplateResponse(BaseModel):
    """Represents a guild template response.

    Reference:
    https://discord.com/developers/docs/resources/guild-template#guild-template-object
    """

    code: str
    """Template code (unique ID)."""

    name: str
    """Template name."""

    description: str | None = None
    """Description for the template."""

    usage_count: int
    """Number of times this template has been used."""

    creator_id: Snowflake
    """ID of the user who created the template."""

    creator: UserResponse
    """User who created the template."""

    created_at: datetime
    """When this template was created."""

    updated_at: datetime
    """When this template was last synced to the source guild."""

    source_guild_id: Snowflake
    """ID of the guild this template is based on."""

    serialized_source_guild: GuildGuildTemplateOut
    """Guild snapshot this template contains."""

    is_dirty: bool | None = None
    """Whether the template has unsynced changes."""
