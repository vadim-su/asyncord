"""Stage Instances Resources.

Stage instances are a way to host live events in Discord. You need to create a stage channel
before creating a stage instance. Stage instances are associated with stage channels.

Reference:
https://discord.com/developers/docs/resources/stage-instance
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.resources import APIResource
from asyncord.client.stage_instances.models.responses import StageInstanceResponse
from asyncord.snowflake import SnowflakeInputType
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.stage_instances.models.requests import (
        CreateStageInstanceRequest,
        UpdateStageInstanceRequest,
    )

__all__ = ('StageInstancesResource',)


class StageInstancesResource(APIResource):
    """Stage Instance Resource.

    Reference:
    https://discord.com/developers/docs/resources/stage-instance
    """

    stage_instances_url = REST_API_URL / 'stage-instances'

    async def get(
        self,
        channel_id: SnowflakeInputType,
    ) -> StageInstanceResponse:
        """Gets the stage instance associated with the Stage channel.

        If exists.

        Reference:
        https://discord.com/developers/docs/resources/stage-instance#get-stage-instance

        Attributes:
            channel_id: The channel id.
        """
        url = self.stage_instances_url / str(channel_id)

        resp = await self._http_client.get(url=url)

        return StageInstanceResponse.model_validate(resp.body)

    async def create_stage_instance(
        self,
        stage_instance_data: CreateStageInstanceRequest,
        reason: str | None = None,
    ) -> StageInstanceResponse:
        """Creates a stage instance associated with the Stage channel.

        Reference:
        https://discord.com/developers/docs/resources/stage-instance#create-stage-instance

        Args:
            stage_instance_data: The stage instance data.
            reason: The reason for creating the stage instance.

        Returns:
            Created stage instance.
        """
        url = self.stage_instances_url

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = stage_instance_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.post(
            url=url,
            payload=payload,
            headers=headers,
        )

        return StageInstanceResponse.model_validate(resp.body)

    async def update(
        self,
        channel_id: SnowflakeInputType,
        stage_instance_data: UpdateStageInstanceRequest,
        reason: str | None = None,
    ) -> StageInstanceResponse:
        """Updates the stage instance associated with the Stage channel.

        Reference:
        https://discord.com/developers/docs/resources/stage-instance#modify-stage-instance

        Args:
            channel_id: The channel id.
            stage_instance_data (UpdateStageInstanceRequest): The stage instance data.
            reason: The reason for updating the stage instance.

        Returns:
            Updated stage instance.
        """
        url = self.stage_instances_url / str(channel_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = stage_instance_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.patch(
            url=url,
            payload=payload,
            headers=headers,
        )

        return StageInstanceResponse.model_validate(resp.body)

    async def delete(
        self,
        channel_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Deletes the stage instance associated with the Stage channel.

        Reference:
        https://discord.com/developers/docs/resources/stage-instance#delete-stage-instance

        Args:
            channel_id: The channel id.
            reason: The reason for deleting the stage instance.
        """
        url = self.stage_instances_url / str(channel_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url=url, headers=headers)
