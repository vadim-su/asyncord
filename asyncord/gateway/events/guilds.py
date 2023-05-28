from datetime import datetime
from typing import Any

from asyncord.client.models.guilds import Guild
from asyncord.client.models.members import Member
from asyncord.client.models.users import User
from asyncord.client.roles import Role
from asyncord.gateway.events.base import GatewayEvent
from asyncord.snowflake import Snowflake


class GuildCreateEvent(GatewayEvent, Guild):
    """Sent when a guild is created/joined.

    This event can be sent in three different scenarios:

        1. When a user is initially connecting, to lazily load and backfill \
            information for all unavailable guilds sent in the Ready event. \
            Guilds that are unavailable due to an outage will send a Guild Delete event.
        2. When a Guild becomes available again to the client.
        3. When the current user joins a new Guild.

    https://discord.com/developers/docs/topics/gateway-events#guild-create
    """

    joined_at: datetime | None = None
    """When this guild was joined at."""

    large: bool | None = None
    """True if this is considered a large guild."""

    unavailable: bool | None = None
    """True if this guild is unavailable due to an outage."""

    member_count: int | None = None
    """Total number of members in this guild."""

    voice_states: list[dict[str, Any]] | None = None
    """States of members currently in voice channels."""

    members: list[Member] | None = None
    """List of guild members."""

    channels: list[dict[str, Any]] | None = None
    """List of channels."""

    threads: list[dict[str, Any]] | None = None
    """List of threads."""

    presences: list[dict[str, Any]] | None = None
    """List of presences."""

    stage_instances: list[dict[str, Any]] | None = None
    """List of stage instances."""

    guild_scheduled_events: list[dict[str, Any]] | None = None
    """List of scheduled events."""


class GuildUpdateEvent(GatewayEvent, Guild):
    """Sent when a guild is updated.

    https://discord.com/developers/docs/topics/gateway-events#guild-update
    """


class GuildDeleteEvent(GatewayEvent):
    """Sent when a guild becomes unavailable, or when the user leaves or is removed from a guild.

    https://discord.com/developers/docs/topics/gateway-events#guild-delete
    """

    id: Snowflake
    """Guild id."""

    unavailable: bool | None = None
    """True if this guild is unavailable due to an outage.

    If the unavailable field is not set, the user was removed from the guild.
    """


class GuildBanAddEvent(GatewayEvent):
    """Sent when a user is banned from a guild.

    https://discord.com/developers/docs/topics/gateway-events#guild-ban-add
    """

    guild_id: Snowflake
    """Guild id."""

    user: User
    """Banned user."""


class GuildBanRemoveEvent(GatewayEvent):
    """Sent when a user is unbanned from a guild.

    https://discord.com/developers/docs/topics/gateway-events#guild-ban-remove
    """

    guild_id: Snowflake
    """Guild id."""

    user: User
    """Unbanned user."""


class GuildEmojisUpdateEvent(GatewayEvent):
    """Sent when a guild's emojis have been updated.

    https://discord.com/developers/docs/topics/gateway-events#guild-emojis-update
    """

    guild_id: Snowflake
    """Guild id."""

    emojis: list[dict[str, Any]]  # FIXME: add Emoji model
    """List of emojis."""


class GuildStickersUpdateEvent(GatewayEvent):
    """Sent when a guild's stickers have been updated.

    https://discord.com/developers/docs/topics/gateway-events#guild-stickers-update
    """

    guild_id: Snowflake
    """Guild id."""

    stickers: list[dict[str, Any]]  # FIXME: add Sticker model
    """List of stickers."""


class GuildIntegrationsUpdateEvent(GatewayEvent):
    """Sent when a guild integration is updated.

    https://discord.com/developers/docs/topics/gateway-events#guild-integrations-update
    """

    guild_id: Snowflake
    """Guild id whose integrations were updated."""


class GuildMemberAddEvent(GatewayEvent, Member):
    """Sent when a new user joins a guild.

    https://discord.com/developers/docs/topics/gateway-events#guild-member-add
    """

    guild_id: Snowflake
    """Guild id."""


class GuildMemberRemoveEvent(GatewayEvent):
    """Sent when a user leaves a guild, or is kicked/banned.

    https://discord.com/developers/docs/topics/gateway-events#guild-member-remove
    """

    guild_id: Snowflake
    """Guild id."""

    user: User
    """Removed user."""


class GuildMemberUpdateEvent(GatewayEvent, Member):
    """Sent when a guild member is updated.

    https://discord.com/developers/docs/topics/gateway-events#guild-member-update
    """

    guild_id: Snowflake
    """Guild id."""

    roles: list[Snowflake]
    """User role ids."""

    user: User
    """User."""

    nick: str | None = None
    """Nick of the user in the guild."""

    avatar: str | None = None
    """Member's guild avatar hash."""

    joined_at: datetime | None = None
    """When the user joined the guild."""

    premium_since: datetime | None = None
    """When the user started boosting the guild."""

    deaf: bool | None = None
    """Whether the user is deafened in voice channels."""

    mute: bool | None = None
    """Whether the user is muted in voice channels."""

    pending: bool | None
    """Whether the user has not yet passed the guild's Membership Screening requirements."""

    communication_disabled_until: datetime | None
    """When the user's timeout will expire.

    User will be able to communicate in the guild again.
    If null or a time in the past if the user is not timed out.
    """


class GuildMembersChunkEvent(GatewayEvent):
    """Sent when a chunk of guild members is received.

    https://discord.com/developers/docs/topics/gateway-events#guild-members-chunk
    """

    guild_id: Snowflake
    """Guild id."""

    members: list[Member]
    """list of guild members"""

    chunk_index: int
    """Chunk index in the expected chunks for this response.

    Should be between 0 and chunk_count (0 <= chunk_index < chunk_count).
    """

    chunk_count: int
    """Total number of expected chunks for this response."""

    not_found: list[Snowflake] | None = None
    """List of user ids that were not found."""

    presences: list[dict[str, Any]] | None = None  # FIXME: add Presence model
    """List of presences of the members."""

    nonce: str | None = None
    """Nonce used in the Guild Members Request."""


class GuildRoleCreateEvent(GatewayEvent):
    """Sent when a guild role is created.

    https://discord.com/developers/docs/topics/gateway-events#guild-role-create
    """

    guild_id: Snowflake
    """Guild id."""

    role: Role
    """Created role."""


class GuildRoleUpdateEvent(GatewayEvent):
    """Sent when a guild role is updated.

    https://discord.com/developers/docs/topics/gateway-events#guild-role-update
    """

    guild_id: Snowflake
    """Guild id."""

    role: Role
    """Updated role."""


class GuildRoleDeleteEvent(GatewayEvent):
    """Sent when a guild role is deleted.

    https://discord.com/developers/docs/topics/gateway-events#guild-role-delete
    """

    guild_id: Snowflake
    """Guild id."""

    role_id: Snowflake
    """Role id."""
