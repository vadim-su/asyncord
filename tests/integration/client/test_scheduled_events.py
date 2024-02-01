import datetime
from typing import AsyncGenerator

import pytest

from asyncord.client.scheduled_events.models.common import (
    EventEntityType,
    EventPrivacyLevel,
)
from asyncord.client.scheduled_events.models.requests import (
    CreateScheduledEventRequest,
    EventEntityMetadata,
    UpdateScheduledEventRequest,
)
from asyncord.client.scheduled_events.models.responses import ScheduledEventResponse
from asyncord.client.scheduled_events.resources import ScheduledEventsResource
from tests.conftest import IntegrationTestData


@pytest.fixture()
async def event(events_res: ScheduledEventsResource) -> AsyncGenerator[ScheduledEventResponse, None]:
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


@pytest.mark.parametrize('event_type', [EventEntityType.EXTERNAL, EventEntityType.VOICE])
async def test_create_event(
    events_res: ScheduledEventsResource,
    integration_data: IntegrationTestData,
    event_type: EventEntityType,
):
    if event_type is EventEntityType.EXTERNAL:
        creation_data = CreateScheduledEventRequest(
            entity_type=event_type,
            name='Test Event',
            description='This is a test event.',
            entity_metadata=EventEntityMetadata(location='https://example.com'),
            privacy_level=EventPrivacyLevel.GUILD_ONLY,
            scheduled_start_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1),
            scheduled_end_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
        )
    else:
        creation_data = CreateScheduledEventRequest(
            entity_type=event_type,
            name='Test Event',
            description='This is a test event.',
            channel_id=integration_data.voice_channel_id,
            privacy_level=EventPrivacyLevel.GUILD_ONLY,
            scheduled_start_time=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1),
        )

    event = await events_res.create(creation_data)
    await events_res.delete(event.id)


async def test_get_event(events_res: ScheduledEventsResource, event: ScheduledEventResponse):
    getted_event = await events_res.get(event.id)
    assert isinstance(getted_event, ScheduledEventResponse)
    assert getted_event.id == event.id
    assert getted_event.name == event.name
    assert getted_event.description == event.description
    assert getted_event.channel_id == event.channel_id
    assert getted_event.entity_type == event.entity_type


async def test_get_event_list(events_res: ScheduledEventsResource, event: ScheduledEventResponse):
    event_list = await events_res.get_list()
    assert isinstance(event_list, list)
    assert len(event_list) >= 1
    assert isinstance(event_list[0], ScheduledEventResponse)


async def test_update_event(events_res: ScheduledEventsResource, event: ScheduledEventResponse):
    updated_event = await events_res.update(event.id, UpdateScheduledEventRequest(name='Updated Event'))
    assert updated_event.name == 'Updated Event'


async def test_get_event_users(events_res: ScheduledEventsResource, event: ScheduledEventResponse):
    users = await events_res.get_event_users(event.id)
    assert isinstance(users, list)
