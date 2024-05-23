"""Models for guild template responses."""

from datetime import datetime

from pydantic import BaseModel

from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.models.permissions import PermissionFlag
from asyncord.client.users.models.responses import UserResponse
from asyncord.color import Color
from asyncord.snowflake import Snowflake


class RoleGuildTemplateOut(BaseModel):
    """Partial role object for guild template response.

    Reference:
    https://canary.discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
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


class GuildGuildTemplateOut(BaseModel):
    """Partial guild object for guild template response.

    Reference:
    https://canary.discord.com/developers/docs/resources/guild-template#guild-template-object-example-guild-template-object
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
    channels: list[ChannelResponse] | None = None
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
    https://canary.discord.com/developers/docs/resources/guild-template#guild-template-object
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
