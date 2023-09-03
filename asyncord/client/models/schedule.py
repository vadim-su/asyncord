"""This module contains models related to scheduled events in a guild."""

from __future__ import annotations

import datetime
import enum
from typing import Self

from pydantic import BaseModel, Field, model_validator

from asyncord.client.models.users import User
from asyncord.snowflake import Snowflake


@enum.unique
class EventPrivacyLevel(enum.IntEnum):
    """Represents a scheduled event's privacy level.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-privacy-level
    """

    PUBLIC = 1
    """Scheduled event is public, guild_id is exposed."""

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


class EventEntityMetadata(BaseModel):
    """Represents a scheduled event's entity metadata.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata
    """

    location: str | None = Field(None, min_length=1, max_length=100)
    """Location of the event."""


class GuildScheduleEvent(BaseModel):
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

    name: str = Field(min_length=1, max_length=100)
    """Name of scheduled event."""

    description: str | None = Field(min_length=1, max_length=1000)
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

    entity_metadata: EventEntityMetadata | None
    """Metadata for the guild scheduled event."""

    creator: User
    """User that created scheduled event."""

    user_count: int | None = None
    """User that created scheduled event."""

    image: str | None = None
    """Cover image hash of scheduled event."""

    # FIXME: #26 This is a temporary solution. Need to replace with multiple models.
    @model_validator(mode='after')
    def validate_entity_type(self) -> Self:
        """Validates the entity type of the scheduled event."""
        match self.entity_type:
            case EventEntityType.EXTERNAL:
                if self.channel_id:
                    raise ValueError('`channel_id` must be None if `entity_type` is EXTERNAL')

                if not self.scheduled_end_time:
                    raise ValueError('`scheduled_end_time` must be set if `entity_type` is EXTERNAL')

                if not self.entity_metadata:
                    raise ValueError('`entity_metadata` must be set if `entity_type` is EXTERNAL')

                if not self.entity_metadata.location:
                    raise ValueError('`entity_metadata.location` must be set if `entity_type` is EXTERNAL')

            case EventEntityType.STAGE_INSTANCE | EventEntityType.VOICE:
                if not self.channel_id:
                    raise ValueError(
                        '`channel_id` must be set if `entity_type` is STAGE_INSTANCE or VOICE',
                    )
                if self.entity_metadata:
                    raise ValueError(
                        '`entity_metadata` must be None if `entity_type` is STAGE_INSTANCE or VOICE',
                    )

        return self
