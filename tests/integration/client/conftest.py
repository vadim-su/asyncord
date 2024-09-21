import datetime
from collections.abc import AsyncGenerator

import pytest

from asyncord.client.scheduled_events.models.common import (
    EventEntityType,
    EventPrivacyLevel,
)
from asyncord.client.scheduled_events.models.requests import (
    CreateScheduledEventRequest,
    EventEntityMetadata,
)
from asyncord.client.scheduled_events.models.responses import ScheduledEventResponse
from asyncord.client.scheduled_events.resources import ScheduledEventsResource


@pytest.fixture
async def event(events_res: ScheduledEventsResource) -> AsyncGenerator[ScheduledEventResponse, None]:
    """Fixture that creates a scheduled event and deletes it after the test."""
    creation_data = CreateScheduledEventRequest(
        entity_type=EventEntityType.EXTERNAL,
        name='Test Event',
        description='This is a test event.',
        entity_metadata=EventEntityMetadata(location='https://example.com'),
        privacy_level=EventPrivacyLevel.GUILD_ONLY,
        scheduled_start_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1),
        scheduled_end_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
    )
    event = await events_res.create(creation_data)
    yield event
    await events_res.delete(event.id)
