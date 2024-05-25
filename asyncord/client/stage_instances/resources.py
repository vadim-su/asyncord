"""Stage Instances Resource.

Reference:
https://canary.discord.com/developers/docs/resources/stage-instance
"""

from __future__ import annotations

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.resources import ClientSubresource
from asyncord.client.stage_instances.models.requests import CreateStageInstanceRequest, UpdateStageInstanceRequest
from asyncord.client.stage_instances.models.responses import StageInstanceResponse
from asyncord.urls import REST_API_URL


class StageInstancesResource(ClientSubresource):
    """Stage Instance Resource.

    These endpoints are for managing stage instances.

    Reference:
    https://canary.discord.com/developers/docs/resources/stage-instance
    """

    stage_instances_url = REST_API_URL / 'stage-instances'

    async def get_stage_instance(
        self,
        channel_id: str,
    ) -> StageInstanceResponse | None:
        """Gets the stage instance associated with the Stage channel.

        If exists.

        Reference:
        https://canary.discord.com/developers/docs/resources/stage-instance#get-stage-instance

        Args:
            channel_id (str): The channel id.
        """
        url = self.stage_instances_url / str(channel_id)

        resp = await self._http_client.get(
            url,
        )

        if resp.body:
            return StageInstanceResponse.model_validate(resp.body)
        return None

    async def create_stage_instance(
        self,
        stage_instance_data: CreateStageInstanceRequest,
        reason: str | None = None,
    ) -> StageInstanceResponse:
        """Creates a stage instance associated with the Stage channel.

        Reference:
        https://canary.discord.com/developers/docs/resources/stage-instance#create-stage-instance

        Args:
            stage_instance_data (CreateStageInstanceRequest): The stage instance data.
            reason (str, optional): The reason for creating the stage instance.
        """
        url = self.stage_instances_url

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = stage_instance_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.post(
            url,
            payload=payload,
            headers=headers,
        )

        return StageInstanceResponse.model_validate(resp.body)

    async def update_stage_instance(
        self,
        channel_id: str,
        stage_instance_data: UpdateStageInstanceRequest,
        reason: str | None = None,
    ) -> StageInstanceResponse:
        """Updates the stage instance associated with the Stage channel.

        Reference:
        https://canary.discord.com/developers/docs/resources/stage-instance#modify-stage-instance

        Args:
            channel_id (str): The channel id.
            stage_instance_data (UpdateStageInstanceRequest): The stage instance data.
            reason (str, optional): The reason for updating the stage instance.
        """
        url = self.stage_instances_url / str(channel_id)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = stage_instance_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.patch(
            url,
            payload=payload,
            headers=headers,
        )

        return StageInstanceResponse.model_validate(resp.body)

    async def delete_stage_instance(
        self,
        channel_id: str,
        reason: str | None = None,
    ) -> None:
        """Deletes the stage instance associated with the Stage channel.

        Reference:
        https://canary.discord.com/developers/docs/resources/stage-instance#delete-stage-instance

        Args:
            channel_id (str): The channel id.
            reason (str, optional): The reason for deleting the stage instance.
        """
        url = self.stage_instances_url / str(channel_id)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(
            url,
            headers=headers,
        )