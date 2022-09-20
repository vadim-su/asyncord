from __future__ import annotations

import enum
import datetime

from pydantic import Field, BaseModel, validator

from asyncord.snowflake import Snowflake
from asyncord.client.models.users import User


class GuildScheduleEvent(BaseModel):
    """Represents a scheduled event in a guild.

    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-structure
    """

    id: Snowflake
    """the id of the scheduled event"""

    guild_id: Snowflake
    """the guild id which the scheduled event belongs to"""

    channel_id: Snowflake | None
    """the channel id in which the scheduled event will be hosted,
    or `None` if entity type is `EXTERNAL`
    """

    creator_id: Snowflake
    """the id of the user that created the scheduled event"""

    name: str = Field(min_length=1, max_length=100)
    """the name of the scheduled event (1-100 characters)"""

    description: str | None = Field(min_length=1, max_length=1000)
    """the description of the scheduled event (1-1000 characters)"""

    scheduled_start_time: datetime.datetime
    """the time the scheduled event will start"""

    scheduled_end_time: datetime.datetime | None
    """the time the scheduled event will end

    `None` if the event does not have a scheduled time to end.
    """

    privacy_level: EventPrivacyLevel
    """the privacy level of the scheduled event"""

    status: EventStatus
    """the status of the scheduled event"""

    entity_type: EventEntityType
    """the entity type of the scheduled event"""

    entity_id: Snowflake | None
    """the id of an entity associated with a guild scheduled event"""

    entity_metadata: EventEntityMetadata | None
    """the metadata for the guild scheduled event"""

    creator: User
    """the user that created the scheduled event"""

    user_count: int | None = None
    """the user that created the scheduled event"""

    image: str | None = None
    """the cover image hash of the scheduled event"""

    @validator('channel_id')
    def check_channel_id(cls, value: Snowflake | None, values) -> Snowflake | None:
        entity_type: EventEntityType = values.get('entity_type')

        if entity_type is EventEntityType.EXTERNAL:
            if value is not None:
                raise ValueError('`channel_id` must be None if `entity_type` is EXTERNAL')

        elif entity_type in {EventEntityType.STAGE_INSTANCE, EventEntityType.VOICE}:
            if value is None:
                raise ValueError(
                    '`channel_id` must not be None if `entity_type` is STAGE_INSTANCE or VOICE',
                )

        return value

    @validator('entity_metadata')
    def check_entity_metadata(cls, value: EventEntityMetadata | None, values) -> EventEntityMetadata | None:
        entity_type: EventEntityType = values.get('entity_type')

        match entity_type:
            case EventEntityType.EXTERNAL:
                if value is None:
                    raise ValueError(
                        '`entity_metadata` must not be None if `entity_type` is EXTERNAL',
                    )

                if value.location is None:
                    raise ValueError(
                        '`entity_metadata.location` must not be None if `entity_type` is EXTERNAL',
                    )

            case EventEntityType.STAGE_INSTANCE | EventEntityType.VOICE:
                if value is not None:
                    raise ValueError(
                        '`entity_metadata` must be None if `entity_type` is STAGE_INSTANCE or VOICE',
                    )

        return value

    @validator('scheduled_end_time')
    def check_scheduled_end_time(cls, value: datetime.datetime | None, values) -> datetime.datetime | None:
        entity_type: EventEntityType = values.get('entity_type')

        if entity_type is EventEntityType.EXTERNAL:
            if not value:
                raise ValueError(
                    '`scheduled_end_time` must not be None if `entity_type` is EXTERNAL',
                )

        return value


@enum.unique
class EventPrivacyLevel(enum.IntEnum):
    """Represents a scheduled event's privacy level.

    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-privacy-level
    """

    PUBLIC = 1
    """the scheduled event is public, the guild_id is exposed"""

    GUILD_ONLY = 2
    """the scheduled event is private, only available to guild members"""


@enum.unique
class EventStatus(enum.IntEnum):
    """Represents a scheduled event's status.

    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-status
    """

    SCHEDULED = 1
    """the scheduled event is scheduled"""

    ACTIVE = 2
    """the scheduled event is currently active"""

    COMPLETED = 3
    """the scheduled event has concluded"""

    CANCELED = 4
    """the scheduled event was canceled"""


@enum.unique
class EventEntityType(enum.IntEnum):
    """Represents a scheduled event's entity type.

    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-types
    """

    STAGE_INSTANCE = 1
    """the scheduled event is associated with a stage instance"""

    VOICE = 2
    """the scheduled event is associated with a voice channel"""

    EXTERNAL = 3
    """the scheduled event is not associated with a guild channel"""


class EventEntityMetadata(BaseModel):
    """Represents a scheduled event's entity metadata.

    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata
    """

    location: str | None = Field(None, min_length=1, max_length=100)
    """location of the event (1-100 characters)"""
