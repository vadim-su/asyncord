from asyncord.client.stage_instances.models.requests import CreateStageInstanceRequest, UpdateStageInstanceRequest
from asyncord.client.stage_instances.resources import StageInstancesResource
from tests.conftest import IntegrationTestData


async def test_stage_instance_cycle(
    stage_instances_res: StageInstancesResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test creating, getting, updating, deleting stage instance."""
    created_stage = await stage_instances_res.create_stage_instance(
        CreateStageInstanceRequest(
            channel_id=integration_data.stage_id,
            topic='Test topic',
        ),
    )

    requested_stage = await stage_instances_res.get_stage_instance(
        integration_data.stage_id,
    )

    assert created_stage.id == requested_stage.id

    updated_stage = await stage_instances_res.update_stage_instance(
        integration_data.stage_id,
        UpdateStageInstanceRequest(
            topic='Updated topic',
        ),
    )
    assert updated_stage.topic != created_stage.topic

    await stage_instances_res.delete_stage_instance(
        integration_data.stage_id,
    )
