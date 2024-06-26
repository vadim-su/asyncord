"""Models for scheduled events requests."""

from __future__ import annotations

import datetime
from typing import Annotated, Self

from pydantic import BaseModel, Field, model_validator

from asyncord.client.scheduled_events.models.common import EventEntityType, EventPrivacyLevel, EventStatus
from asyncord.snowflake import SnowflakeInputType

__all__ = (
    'CreateScheduledEventRequest',
    'EventEntityMetadata',
    'UpdateScheduledEventRequest',
)


class EventEntityMetadata(BaseModel):
    """Metadata for the guild scheduled event.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-metadata
    """

    location: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    """Location of the event."""


class CreateScheduledEventRequest(BaseModel):
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

    channel_id: SnowflakeInputType | None = None
    """Channel id of the scheduled event."""

    entity_metadata: EventEntityMetadata | None = None
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
        return _validate_entity_type(self)


class UpdateScheduledEventRequest(BaseModel):
    """Represents a scheduled event data to update.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-update
    """

    channel_id: SnowflakeInputType | None = None
    """Channel id of the scheduled event."""

    entity_metadata: EventEntityMetadata | None = None
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
        return _validate_entity_type(self)


def _validate_entity_type[ModelObjT: UpdateScheduledEventRequest | CreateScheduledEventRequest](
    model_obj: ModelObjT,
) -> ModelObjT:
    """Validates the entity type of the scheduled event."""
    match model_obj.entity_type:
        case None:
            # can't validate if entity type is not set
            return model_obj

        case EventEntityType.EXTERNAL:
            # fmt: off
            has_needed_fields = bool(
                model_obj.entity_metadata
                and model_obj.entity_metadata.location
                and model_obj.scheduled_end_time,
            )
            # fmt: on
            if not has_needed_fields:
                required_fields = ('entity_metadata', 'entity_metadata.location', 'scheduled_end_time')
                err_msg = f'EXTERNAL type requires the fields {required_fields} to be set'
                raise ValueError(err_msg)

        case EventEntityType.STAGE_INSTANCE | EventEntityType.VOICE:
            if not model_obj.channel_id:
                raise ValueError('`channel_id` must be set if `entity_type` is STAGE_INSTANCE or VOICE')

        case _:  # pragma: no cover
            raise ValueError('Invalid entity type')  # unreachable in theory

    return model_obj
