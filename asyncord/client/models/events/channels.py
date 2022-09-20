from typing import Any
from datetime import datetime

from asyncord.snowflake import Snowflake
from asyncord.client.models.members import Member
from asyncord.client.models.channels import Channel, ChannelType, ThreadMember
from asyncord.client.models.events.base import GatewayEvent


class ChannelCreateEvent(GatewayEvent, Channel):
    """https://discord.com/developers/docs/topics/gateway#channel-create"""


class ChannelUpdateEvent(GatewayEvent, Channel):
    """https://discord.com/developers/docs/topics/gateway#channel-update"""


class ChannelDeleteEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#channel-delete"""

    id: Snowflake
    """channel id"""

    type: ChannelType
    """The type of channel."""

    guild_id: Snowflake
    """The id of the guild."""

    parent_id: Snowflake | None = None
    """Parent category or channel id.

    For guild channels: id of the parent category for a channel.
    For threads: id of the text channel this thread was created.

    Each parent category can contain up to 50 channels.
    """


class ChannelPinsUpdateEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#channel-pins-update"""

    guild_id: Snowflake
    """the id of the guild"""

    channel_id: Snowflake
    """the id of the channel"""

    last_pin_timestamp: datetime | None
    """the time at which the most recent pinned message was pinned"""


class ThreadCreateEvent(GatewayEvent, Channel):
    """https://discord.com/developers/docs/topics/gateway#thread-create"""
    # FIXME: read the docs and add the missing thread member object

    newly_created: bool
    """when a thread is created"""


class ThreadUpdateEvent(GatewayEvent, Channel):
    """https://discord.com/developers/docs/topics/gateway#thread-update"""


class ThreadDeleteEvent(GatewayEvent, Channel):
    """https://discord.com/developers/docs/topics/gateway#thread-delete"""


class ThreadListSyncEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#thread-list-sync"""

    guild_id: Snowflake
    """the id of the guild"""

    channel_ids: list[Snowflake]
    """the parent channel ids whose threads are being synced.
    If omitted, then threads were synced for the entire guild.
    This array may contain channel_ids that have no active threads as well,
    so you know to clear that data.
    """

    threads: list[dict[str, Any]]  # FIXME: Add thread object
    """all active threads in the given channels that the current user can access"""

    members: list[Member]


class ThreadMemberUpdate(ThreadMember):
    guild_id: Snowflake
    """the id of the guild"""

    presence: dict[str, Any] | None = None  # FIXME: Add presence object
    """https://discord.com/developers/docs/topics/gateway#presence"""


class ThreadMemberUpdateEvent(GatewayEvent, ThreadMemberUpdate):
    """https://discord.com/developers/docs/topics/gateway#thread-member-update"""


class ThreadMembersUpdateEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#thread-members-update"""

    id: Snowflake
    """the id of the thread"""

    guild_id: Snowflake
    """the id of the guild"""

    member_count: int
    """the approximate number of members in the thread, capped at 50"""

    added_members: list[ThreadMemberUpdate] | None = None
    """the users who were added to the thread"""

    removed_member_ids: list[Snowflake] | None = None
    """the ids of the users who were removed from the thread"""
