"""This module contains models related to scheduled events in a guild."""

from __future__ import annotations

import datetime

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel

from asyncord.client.members.models.responses import MemberResponse
from asyncord.client.scheduled_events.models.common import EventEntityType, EventPrivacyLevel, EventStatus
from asyncord.client.users.models.responses import UserResponse
from asyncord.snowflake import Snowflake

__all__ = (
    'EventEntityMetadataOut',
    'ScheduledEventResponse',
    'ScheduledEventUserResponse',
)


class EventEntityMetadataOut(BaseModel):
    """Metadata for the guild scheduled event.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata
    """

    location: str | None = None
    """Location of the event."""


class ScheduledEventResponse(BaseModel):
    """Represents a scheduled event in a guild.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-structure
    """

    id: Snowflake
    """ID of scheduled event."""

    guild_id: Snowflake
    """Guild id which scheduled event belongs to."""

    channel_id: Snowflake | None
    """Channel id in which scheduled event will be hosted.

    Should be `None` if entity type is `EXTERNAL`.
    """

    creator_id: Snowflake
    """Id of user that created scheduled event."""

    name: str
    """Name of scheduled event."""

    description: str | None
    """Description of scheduled event"""

    scheduled_start_time: datetime.datetime
    """Time scheduled event will start."""

    scheduled_end_time: datetime.datetime | None
    """Time scheduled event will end.

    `None` if event does not have a scheduled time to end.
    """

    privacy_level: FallbackAdapter[EventPrivacyLevel]
    """Privacy level of scheduled event."""

    status: FallbackAdapter[EventStatus]
    """Status of scheduled event."""

    entity_type: FallbackAdapter[EventEntityType]
    """Entity type of scheduled event."""

    entity_id: Snowflake | None
    """Id of an entity associated with a guild scheduled event."""

    entity_metadata: EventEntityMetadataOut | None
    """Metadata for the guild scheduled event."""

    creator: UserResponse | None = None
    """User that created scheduled event."""

    user_count: int | None = None
    """User that created scheduled event."""

    image: str | None = None
    """Cover image hash of scheduled event."""


class ScheduledEventUserResponse(BaseModel):
    """Represents a user that has signed up for a guild scheduled event."""

    guild_scheduled_event_id: Snowflake
    """Scheduled event id which user subscribed to."""

    user: UserResponse
    """User which subscribed to an event."""

    member: MemberResponse | None = None
    """Guild member data for this user for the guild which this event belongs to."""
