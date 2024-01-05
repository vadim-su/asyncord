"""This module contains models related to scheduled events in a guild."""

from __future__ import annotations

import datetime
import enum
from typing import Self

from pydantic import BaseModel, Field, model_validator

from asyncord.client.members.models import MemberOutput
from asyncord.client.users.models import UserOutput
from asyncord.snowflake import Snowflake, SnowflakeInput


@enum.unique
class EventPrivacyLevel(enum.IntEnum):
    """Represents a scheduled event's privacy level.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-privacy-level
    """

    GUILD_ONLY = 2
    """Scheduled event is private, only available to guild members."""


@enum.unique
class EventStatus(enum.IntEnum):
    """Represents a scheduled event's status.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-status
    """

    SCHEDULED = 1
    """Scheduled event is scheduled."""

    ACTIVE = 2
    """Scheduled event is currently active."""

    COMPLETED = 3
    """Scheduled event has concluded."""

    CANCELED = 4
    """Scheduled event was canceled."""


@enum.unique
class EventEntityType(enum.IntEnum):
    """Represents a scheduled event's entity type.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-types
    """

    STAGE_INSTANCE = 1
    """Scheduled event is associated with a stage instance."""

    VOICE = 2
    """Scheduled event is associated with a voice channel."""

    EXTERNAL = 3
    """Scheduled event is not associated with a guild channel."""


class EventEntityMetadataInput(BaseModel):
    """Represents a scheduled event's entity metadata.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata
    """

    location: str | None = Field(None, min_length=1, max_length=100)
    """Location of the event."""


class CreateScheduledEventInput(BaseModel):
    """Represents a scheduled event data to create.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-create
    """

    entity_type: EventEntityType
    """Entity type of the scheduled event."""

    name: str
    """Name of the scheduled event."""

    description: str | None = None
    """Description of the scheduled event."""

    channel_id: SnowflakeInput | None = None
    """Channel id of the scheduled event."""

    entity_metadata: EventEntityMetadataInput | None = None
    """Entity metadata of the scheduled event."""

    privacy_level: EventPrivacyLevel
    """Privacy level of the scheduled event."""

    scheduled_start_time: datetime.datetime
    """Time to schedule the scheduled event in ISO8601 format."""

    scheduled_end_time: datetime.datetime | None = None
    """Time when the scheduled event is scheduled to end in ISO8601 format."""

    image: str | None = None
    """Cover image hash of scheduled event."""

    @model_validator(mode='after')
    def validate_entity_type(self) -> Self:
        """Validates the entity type of the scheduled event."""
        if self.entity_type is EventEntityType.EXTERNAL:
            if not self.entity_metadata:
                raise ValueError('`entity_metadata` must be set if `entity_type` is EXTERNAL')

            if not self.entity_metadata.location:
                raise ValueError('`entity_metadata.location` must be set if `entity_type` is EXTERNAL')

            if not self.scheduled_end_time:
                raise ValueError('`scheduled_end_time` must be set if `entity_type` is EXTERNAL')

        elif not self.channel_id:
            raise ValueError('`channel_id` must be set if `entity_type` is STAGE_INSTANCE or VOICE')

        return self


class UpdateScheduledEventInput(BaseModel):
    """Represents a scheduled event data to update.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-update
    """

    channel_id: SnowflakeInput | None = None
    """Channel id of the scheduled event."""

    entity_metadata: EventEntityMetadataInput | None = None
    """Entity metadata of the scheduled event."""

    name: str | None = None
    """Name of the scheduled event."""

    privacy_level: EventPrivacyLevel | None = None
    """Privacy level of the scheduled event."""

    scheduled_start_time: datetime.datetime | None = None
    """Time to schedule the scheduled event in ISO8601 format."""

    scheduled_end_time: datetime.datetime | None = None
    """Time when the scheduled event is scheduled to end in ISO8601 format."""

    description: str | None = None
    """Description of the scheduled event."""

    entity_type: EventEntityType | None = None
    """Entity type of the scheduled event."""

    status: EventStatus | None = None
    """Status of the scheduled event."""

    image: str | None = None
    """Cover image hash of scheduled event."""

    @model_validator(mode='after')
    def validate_entity_type(self) -> Self:
        """Validates the entity type of the scheduled event."""
        if not self.entity_type:
            # can't validate if entity type is not set
            return self

        if self.entity_type is EventEntityType.EXTERNAL:
            if not self.entity_metadata:
                raise ValueError('`entity_metadata` must be set if `entity_type` is EXTERNAL')

            if not self.entity_metadata.location:
                raise ValueError('`entity_metadata.location` must be set if `entity_type` is EXTERNAL')

            if not self.scheduled_end_time:
                raise ValueError('`scheduled_end_time` must be set if `entity_type` is EXTERNAL')

        elif not self.channel_id:
            raise ValueError('`channel_id` must be set if `entity_type` is STAGE_INSTANCE or VOICE')

        return self


class ScheduledEventOutput(BaseModel):
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

    privacy_level: EventPrivacyLevel
    """Privacy level of scheduled event."""

    status: EventStatus
    """Status of scheduled event."""

    entity_type: EventEntityType
    """Entity type of scheduled event."""

    entity_id: Snowflake | None
    """Id of an entity associated with a guild scheduled event."""

    entity_metadata: EventEntityMetadataInput | None
    """Metadata for the guild scheduled event."""

    creator: UserOutput | None = None
    """User that created scheduled event."""

    user_count: int | None = None
    """User that created scheduled event."""

    image: str | None = None
    """Cover image hash of scheduled event."""


class ScheduledEventUserOutput(BaseModel):
    """Represents a user that has signed up for a guild scheduled event."""

    guild_scheduled_event_id: Snowflake
    """Scheduled event id which user subscribed to."""

    user: UserOutput
    """User which subscribed to an event."""

    member: MemberOutput | None = None
    """Guild member data for this user for the guild which this event belongs to."""
