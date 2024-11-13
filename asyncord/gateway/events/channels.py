"""This module contains the channel events for the gateway."""

import datetime
from typing import Any

from fbenum.adapter import FallbackAdapter

from asyncord.client.channels.models.common import ChannelType
from asyncord.client.channels.models.responses import ChannelResponse, ThreadMemberResponse
from asyncord.client.members.models.responses import MemberResponse
from asyncord.client.threads.models.common import ThreadType
from asyncord.client.threads.models.responses import ThreadResponse
from asyncord.gateway.events.base import GatewayEvent
from asyncord.snowflake import Snowflake

__all__ = (
    'ChannelCreateEvent',
    'ChannelDeleteEvent',
    'ChannelPinsUpdateEvent',
    'ChannelUpdateEvent',
    'ThreadCreateEvent',
    'ThreadDeleteEvent',
    'ThreadListSyncEvent',
    'ThreadMemberUpdateEvent',
    'ThreadMembersUpdateEvent',
    'ThreadUpdateEvent',
)


class ChannelCreateEvent(GatewayEvent, ChannelResponse):
    """Sent when a new guild channel is created.

    Relevant to the current user.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#channel-create
    """


class ChannelUpdateEvent(GatewayEvent, ChannelResponse):
    """Sent when a channel is updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#channel-update
    """


class ChannelDeleteEvent(GatewayEvent):
    """Sent when a channel is deleted.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#channel-delete
    """

    id: Snowflake
    """Channel id."""

    type: FallbackAdapter[ChannelType]
    """Channel type."""

    guild_id: Snowflake
    """Guild id."""

    parent_id: Snowflake | None = None
    """Parent category or channel id.

    For guild channels: id of the parent category for a channel.
    For threads: id of the text channel this thread was created.

    Each parent category can contain up to 50 channels.
    """


class ChannelPinsUpdateEvent(GatewayEvent):
    """Sent when a channel's pins are updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#channel-pins-update
    """

    guild_id: Snowflake
    """Guild id."""

    channel_id: Snowflake
    """the id of the channel"""

    last_pin_timestamp: datetime.datetime | None
    """the time at which the most recent pinned message was pinned"""


class ThreadCreateEvent(GatewayEvent, ChannelResponse):
    """Sent when a thread is created or when the current user is added to a private thread.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#thread-create
    """

    newly_created: bool
    """When a thread is created."""

    thread_member: ThreadMemberResponse | None = None
    """Is sent when the user is added to a private thread."""


class ThreadUpdateEvent(GatewayEvent, ChannelResponse):
    """Sent when a thread is updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#thread-update
    """


class ThreadDeleteEvent(GatewayEvent):
    """Sent when a thread is deleted.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#thread-delete
    """

    id: Snowflake
    """Channel id."""

    type: FallbackAdapter[ThreadType]
    """Type of channel."""

    guild_id: Snowflake | None = None
    """Guild id.

    May be missing for some thread objects received over gateway guild dispatches.
    """

    parent_id: Snowflake
    """Id of the parent channel for a thread."""


class ThreadListSyncEvent(GatewayEvent):
    """Sent when the current user gains access to a channel that contains threads.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#thread-list-sync
    """

    guild_id: Snowflake
    """Guild id"""

    channel_ids: list[Snowflake]
    """Parent channel ids whose threads are being synced.

    If omitted, then threads were synced for the entire guild.

    This array may contain channel_ids that have no active threads as well,
    so you know to clear that data.
    """

    threads: list[ThreadResponse]
    """All active threads in the given channels that the current user can access."""

    members: list[MemberResponse]
    """All thread member objects from the synced threads for the current user.

    Indicating which threads the current user has been added to.
    """


class ThreadMemberUpdateEvent(GatewayEvent, ThreadMemberResponse):
    """Sent when a thread member is updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#thread-member-update
    """

    guild_id: Snowflake
    """Guild id."""


class ThreadMemberUpdate(ThreadMemberResponse):
    """Sent when a thread member is updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#thread-members-update-thread-members-update-event-fields
    """

    member: MemberResponse  # type: ignore
    """Member object."""

    presence: dict[str, Any] | None = None  # FIXME: Add presence object
    """Presence object.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#presence
    """


class ThreadMembersUpdateEvent(GatewayEvent):
    """Sent when the thread member object for the current user is updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#thread-members-update
    """

    id: Snowflake
    """the id of the thread"""

    guild_id: Snowflake
    """Guild id."""

    member_count: int
    """Approximate number of members in the thread.

    Limited to 50 members.
    """

    added_members: list[ThreadMemberUpdate] | None = None
    """Users who were added to the thread."""

    removed_member_ids: list[Snowflake] | None = None
    """Users ids who were removed from the thread."""
