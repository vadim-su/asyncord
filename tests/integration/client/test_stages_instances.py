from collections.abc import AsyncGenerator

import pytest

from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.stage_instances.models.requests import CreateStageInstanceRequest, UpdateStageInstanceRequest
from asyncord.client.stage_instances.models.responses import StageInstanceResponse
from asyncord.client.stage_instances.resources import StageInstancesResource


@pytest.fixture
async def stage(
    stage_channel: ChannelResponse,
    stage_instances_res: StageInstancesResource,
) -> AsyncGenerator[StageInstanceResponse, None]:
    """Fixture for creating stage instance and deleting it after test."""
    stage = await stage_instances_res.create_stage_instance(
        CreateStageInstanceRequest(
            channel_id=stage_channel.id,
            topic='Test topic',
        ),
    )
    yield stage
    await stage_instances_res.delete(stage_channel.id)


async def test_stage_instance_lifecycle(
    stage_channel: ChannelResponse,
    stage: StageInstanceResponse,
    stage_instances_res: StageInstancesResource,
) -> None:
    """Test full lifecycle of stage instance."""
    requested_stage = await stage_instances_res.get(stage_channel.id)

    assert stage.id == requested_stage.id

    updated_stage = await stage_instances_res.update(
        stage_channel.id,
        UpdateStageInstanceRequest(topic='Updated topic'),
    )
    assert updated_stage.topic == 'Updated topic'
