from collections.abc import AsyncGenerator

import pytest

from asyncord.client.channels.models.requests.creation import CreateStageChannelRequest
from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.stage_instances.models.requests import CreateStageInstanceRequest, UpdateStageInstanceRequest
from asyncord.client.stage_instances.models.responses import StageInstanceResponse
from asyncord.client.stage_instances.resources import StageInstancesResource
from tests.conftest import IntegrationTestData


@pytest.fixture()
async def stage_channel(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> AsyncGenerator[ChannelResponse, None]:
    """Fixture for creating channel and deleting it after test."""
    channel = await channel_res.create_channel(
        integration_data.guild_id,
        CreateStageChannelRequest(name='Test stage channel'),
    )
    yield channel
    await channel_res.delete(channel.id)


@pytest.fixture()
async def stage(
    stage_channel: ChannelResponse,
    stage_instances_res: StageInstancesResource,
    integration_data: IntegrationTestData,
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


async def test_stage_instance_lifecicle(
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
