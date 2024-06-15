"""This module contains models for thread responses."""

import datetime

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel

from asyncord.client.channels.models.common import ChannelFlag
from asyncord.client.channels.models.responses import (
    ThreadMemberResponse,
)
from asyncord.client.threads.models.common import ThreadType
from asyncord.snowflake import Snowflake

__all__ = (
    'ThreadMetadataOut',
    'ThreadResponse',
    'ThreadsResponse',
)


class ThreadMetadataOut(BaseModel):
    """Thread metadata object.

    Reference:
    https://discord.com/developers/docs/resources/channel#thread-metadata-object
    """

    archived: bool
    """Whether the thread is archived."""

    auto_archive_duration: int
    """Duration in minutes to automatically archive the thread after recent activity.

    Can be set to: 60, 1440, 4320, 10080.
    """

    archive_timestamp: datetime.datetime
    """Timestamp when the thread's archive status was last changed.

    Used for calculating recent activity.
    """

    locked: bool
    """Whether the thread is locked.

    When a thread is locked, only users with `MANAGE_THREADS` can unarchive it.
    """

    invitable: bool | None = None
    """Whether non-moderators can add other non-moderators to a thread.

    Only available on private threads.
    """

    create_timestamp: datetime.datetime | None = None
    """Timestamp when the thread was created.

    Only populated for threads created after 2022-01-09.
    """


class ThreadResponse(BaseModel):
    """Thread object.

    Reference:
    https://discord.com/developers/docs/resources/channel#channel-object-channel-structure
    """

    id: Snowflake
    """Channel id."""

    type: FallbackAdapter[ThreadType]
    """Type of channel."""

    guild_id: Snowflake | None = None
    """Guild id.

    May be missing for some thread objects received over gateway guild dispatches.
    """

    name: str | None = None
    """Channel name (1-100 characters)"""

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    last_message_id: Snowflake | None = None
    """Last id message sent in this channel.

    May not point to an existing or valid message.
    """

    rate_limit_per_user: int | None = None
    """Amount of seconds a user has to wait before sending another message.

    Should be between 0 and 21600.

    Bots, as well as users with the permission manage_messages or manage_channel,
    are unaffected. `rate_limit_per_user` also applies to thread creation.
    Users can send one message and create one thread during each
    `rate_limit_per_user` interval.
    """

    flags: ChannelFlag | None = None
    """Flags for the channel."""

    owner_id: Snowflake
    """Creator id for the thread."""

    parent_id: Snowflake
    """Id of the parent channel for a thread."""

    last_pin_timestamp: datetime.datetime | None = None
    """Timestamp when the last pinned message was pinned.

    This may be null in events such as GUILD_CREATE when a message is not pinned.
    """

    message_count: int
    """Approximate count of messages in a thread, stops counting at 50."""

    total_message_sent: int
    """Number of messages ever sent in a thread.

    It's similar to message_count on message creation, but will not decrement
    the number when a message is deleted.
    """

    member_count: int
    """Approximate count of users in a thread, stops counting at 50."""

    member: ThreadMemberResponse | None = None
    """Thread member object for the current user.

    If they have joined the thread, only included on certain API endpoints.
    """

    applied_tags: list[Snowflake] | None = None
    """Set of tag ids that have been applied to a thread."""

    thread_metadata: ThreadMetadataOut
    """Thread-specific fields not needed by other channels."""


class ThreadsResponse(BaseModel):
    """Guild active threads response object.

    Reference:
    https://discord.com/developers/docs/resources/guild#list-active-guild-threads-response-body
    """

    threads: list[ThreadResponse]
    """List of thread objects."""

    members: list[ThreadMemberResponse]
    """List of thread member objects."""

    has_more: bool | None = None
    """Whether there are potentially additional threads that could be returned on a subsequent call."""
