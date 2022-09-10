
from typing import Any
from datetime import datetime

from asyncord.snowflake import Snowflake
from asyncord.client.roles import Role
from asyncord.client.models.users import User
from asyncord.client.models.guilds import Guild
from asyncord.client.models.member import Member
from asyncord.client.models.gateway_events import GatewayEvent


class GuildCreateEvent(GatewayEvent, Guild):
    """https://discord.com/developers/docs/topics/gateway#guild-create

    This event can be sent in three different scenarios:

        1. When a user is initially connecting, to lazily load and backfill \
            information for all unavailable guilds sent in the Ready event. \
            Guilds that are unavailable due to an outage will send a Guild Delete event.
        2. When a Guild becomes available again to the client.
        3. When the current user joins a new Guild.
    """
    joined_at: datetime | None = None
    """when this guild was joined at"""

    large: bool | None = None
    """true if this is considered a large guild"""

    unavailable: bool | None = None
    """true if this guild is unavailable due to an outage"""

    member_count: int | None = None
    """total number of members in this guild"""

    voice_states: list[dict[str, Any]] | None = None
    """states of members currently in voice channels"""

    members: list[Member] | None = None
    """list of guild members"""

    channels: list[dict[str, Any]] | None = None
    """list of channels"""

    threads: list[dict[str, Any]] | None = None
    """list of threads"""

    presences: list[dict[str, Any]] | None = None
    """list of presences"""

    stage_instances: list[dict[str, Any]] | None = None
    """list of stage instances"""

    guild_scheduled_events: list[dict[str, Any]] | None = None
    """list of scheduled events"""


class GuildUpdateEvent(GatewayEvent, Guild):
    """https://discord.com/developers/docs/topics/gateway#guild-update"""


class GuildDeleteEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-delete"""

    id: Snowflake
    """guild id"""

    unavailable: bool | None = None
    """true if this guild is unavailable due to an outage
    If the unavailable field is not set, the user was removed from the guild.
    """


class GuildBanAddEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-ban-add"""

    guild_id: Snowflake
    """the id of the guild"""

    user: User
    """the banned user"""


class GuildBanRemoveEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-ban-remove"""

    guild_id: Snowflake
    """the id of the guild"""

    user: User
    """the unbanned user"""


class GuildEmojisUpdateEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-emojis-update"""

    guild_id: Snowflake
    """the id of the guild"""

    emojis: list[dict[str, Any]]  # FIXME: add Emoji model
    """list of emojis"""


class GuildStickersUpdateEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-stickers-update"""

    guild_id: Snowflake
    """the id of the guild"""

    stickers: list[dict[str, Any]]  # FIXME: add Sticker model
    """list of stickers"""


class GuildIntegrationsUpdateEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-integrations-update"""

    guild_id: Snowflake
    """id of the guild whose integrations were updated"""


class GuildMemberAddEvent(GatewayEvent, Member):
    """https://discord.com/developers/docs/topics/gateway#guild-member-add"""

    guild_id: Snowflake
    """id of the guild"""


class GuildMemberRemoveEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-member-remove"""

    guild_id: Snowflake
    """id of the guild"""

    user: User
    """the user who was removed"""


class GuildMemberUpdateEvent(GatewayEvent, Member):
    """https://discord.com/developers/docs/topics/gateway#guild-member-update"""

    guild_id: Snowflake
    """the id of the guild"""

    roles: list[Snowflake]
    """user role ids"""

    user: User
    """the user"""

    nick: str | None = None
    """nick of the user in the guild"""

    avatar: str | None = None
    """the member's guild avatar hash"""

    joined_at: datetime | None = None
    """when the user joined the guild"""

    premium_since: datetime | None = None
    """when the user started boosting the guild"""

    deaf: bool | None = None
    """whether the user is deafened in voice channels"""

    mute: bool | None = None
    """whether the user is muted in voice channels"""

    pending: bool | None
    """whether the user has not yet passed the guild's Membership Screening requirements"""

    communication_disabled_until: datetime | None
    """when the user's timeout will expire and the user will be able to
    communicate in the guild again, null or a time in the past if the user
    is not timed out
    """


class GuildMembersChunkEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-members-chunk"""

    guild_id: Snowflake
    """id of the guild"""

    members: list[Member]
    """list of guild members"""

    chunk_index: int
    """the chunk index in the expected chunks for this response
    (0 <= chunk_index < chunk_count)
    """

    chunk_count: int
    """the total number of expected chunks for this response"""

    not_found: list[Snowflake] | None = None
    """list of user ids that were not found"""

    presences: list[dict[str, Any]] | None = None  # FIXME: add Presence model
    """list of presences of the members"""

    nonce: str | None = None
    """the nonce used in the Guild Members Request"""


class GuildRoleCreateEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-role-create"""

    guild_id: Snowflake
    """id of the guild"""

    role: Role
    """the role created"""


class GuildRoleUpdateEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-role-update"""

    guild_id: Snowflake
    """id of the guild"""

    role: Role
    """the role updated"""


class GuildRoleDeleteEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-role-delete"""

    guild_id: Snowflake
    """id of the guild"""

    role_id: Snowflake
    """id of the role"""

# TODO: add guild scheduled event models
