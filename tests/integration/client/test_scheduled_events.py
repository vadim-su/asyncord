import contextlib
import datetime
from typing import Any

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


@pytest.mark.parametrize('event_type', [EventEntityType.EXTERNAL, EventEntityType.VOICE])
async def test_create_event(
    events_res: ScheduledEventsResource,
    integration_data: IntegrationTestData,
    event_type: EventEntityType,
) -> None:
    """Test creating a scheduled event."""
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


async def test_get_event(
    events_res: ScheduledEventsResource,
    event: ScheduledEventResponse,
) -> None:
    """Test getting a scheduled event."""
    getted_event = await events_res.get(event.id)
    assert isinstance(getted_event, ScheduledEventResponse)
    assert getted_event.id == event.id
    assert getted_event.name == event.name
    assert getted_event.description == event.description
    assert getted_event.channel_id == event.channel_id
    assert getted_event.entity_type == event.entity_type


async def test_get_event_list(
    events_res: ScheduledEventsResource,
    event: ScheduledEventResponse,
) -> None:
    """Test getting a list of scheduled events."""
    event_list = await events_res.get_list()
    assert isinstance(event_list, list)
    assert len(event_list) >= 1
    assert isinstance(event_list[0], ScheduledEventResponse)


async def test_update_event(
    events_res: ScheduledEventsResource,
    event: ScheduledEventResponse,
) -> None:
    """Test updating a scheduled event."""
    updated_event = await events_res.update(
        event_id=event.id,
        event_data=UpdateScheduledEventRequest(name='Updated Event'),
    )
    assert updated_event.name == 'Updated Event'


async def test_get_event_users(
    events_res: ScheduledEventsResource,
    event: ScheduledEventResponse,
) -> None:
    """Test getting a list of users who have signed up for a scheduled event."""
    users = await events_res.get_event_users(event.id)
    assert isinstance(users, list)


@pytest.mark.parametrize(
    'event_type',
    [pytest.param(event_type, id=event_type.name) for event_type in EventEntityType],
)
@pytest.mark.parametrize(
    'model_fields',
    [
        pytest.param(
            {},
            id='without_fields',
        ),
        pytest.param(
            {
                'entity_metadata': {'location': 'https://example.com'},
            },
            id='with_entity_metadata',
        ),
        pytest.param(
            {
                'scheduled_end_time': datetime.datetime.now(datetime.UTC),
            },
            id='with_end_time',
        ),
        pytest.param(
            {
                'entity_metadata': {'location': 'https://example.com'},
                'scheduled_end_time': datetime.datetime.now(datetime.UTC),
            },
            id='with_all_necessary_fields',
        ),
    ],
)
@pytest.mark.parametrize('channel_id', [None, 1234567890])
async def test_envent_type_validation_on_creation(
    event_type: EventEntityType,
    model_fields: dict[str, Any],
    channel_id: int | None,
) -> None:
    """Test entity type validation on creation."""
    entity_metada: dict[str, Any] | None = model_fields.get('entity_metadata')
    # fmt: off
    has_fields = bool(
        entity_metada
        and model_fields.get('scheduled_end_time')
        and entity_metada.get('location'),
    )
    # fmt: on

    err_context = contextlib.nullcontext()

    if event_type is EventEntityType.EXTERNAL:
        if not has_fields:
            err_context = pytest.raises(
                ValueError,
                match='EXTERNAL type requires the fields',
            )

    elif not channel_id:
        err_context = pytest.raises(ValueError, match='`channel_id` must be set if')

    with err_context:
        CreateScheduledEventRequest(
            name='Test Event',
            privacy_level=EventPrivacyLevel.GUILD_ONLY,
            scheduled_start_time=datetime.datetime.now(datetime.UTC),
            entity_type=event_type,
            channel_id=channel_id,
            **model_fields,
        )


@pytest.mark.parametrize(
    'event_type',
    [pytest.param(event_type, id=event_type.name) for event_type in EventEntityType] + [None],
)
@pytest.mark.parametrize(
    'model_fields',
    [
        pytest.param(
            {},
            id='without_fields',
        ),
        pytest.param(
            {
                'entity_metadata': {'location': 'https://example.com'},
            },
            id='with_entity_metadata',
        ),
        pytest.param(
            {
                'scheduled_end_time': datetime.datetime.now(datetime.UTC),
            },
            id='with_end_time',
        ),
        pytest.param(
            {
                'entity_metadata': {'location': 'https://example.com'},
                'scheduled_end_time': datetime.datetime.now(datetime.UTC),
            },
            id='with_all_necessary_fields',
        ),
    ],
)
@pytest.mark.parametrize('channel_id', [None, 1234567890])
async def test_envent_type_validation_on_updating(
    event_type: EventEntityType | None,
    model_fields: dict[str, Any],
    channel_id: int | None,
) -> None:
    """Test entity type validation on updating.

    It differs from the creation test because event type can be None for updating.
    """
    entity_metada: dict[str, Any] | None = model_fields.get('entity_metadata')
    # fmt: off
    has_fields = bool(
        entity_metada
        and model_fields.get('scheduled_end_time')
        and entity_metada.get('location'),
    )
    # fmt: on

    err_context = contextlib.nullcontext()

    if event_type is EventEntityType.EXTERNAL:
        if not has_fields:
            err_context = pytest.raises(
                ValueError,
                match='EXTERNAL type requires the fields',
            )

    elif event_type and not channel_id:
        err_context = pytest.raises(ValueError, match='`channel_id` must be set if')

    with err_context:
        UpdateScheduledEventRequest(
            entity_type=event_type,
            channel_id=channel_id,
            **model_fields,
        )
