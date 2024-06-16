"""This module contains resources to perform actions on interactions.

Currently, the only action is to send a response to an interaction. Discord don't
provide any other actions for interactions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.interactions.models.requests import (
    INTERACTIONS_CAN_CONTAIN_FILES,
    InteractionRespPongRequest,
    RootInteractionResponse,
)
from asyncord.client.models.attachments import make_attachment_payload
from asyncord.client.resources import APIResource
from asyncord.snowflake import SnowflakeInputType
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.interactions.models.requests import InteractionResponseRequestType
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('InteractionResource',)


class InteractionResource(APIResource):
    """Resource to perform actions on interactions."""

    interactions_url = REST_API_URL / 'interactions'

    async def send_response(
        self,
        interaction_id: SnowflakeInputType,
        interaction_token: str,
        interaction_response: InteractionResponseRequestType,
    ) -> None:
        """Send a response to an interaction.

        Args:
            interaction_id: Interaction ID.
            interaction_token: Interaction token.
            interaction_response: Response to send to the interaction.
        """
        url = self.interactions_url / str(interaction_id) / interaction_token / 'callback'
        if isinstance(interaction_response, InteractionRespPongRequest):
            # Pong response doesn't have a data key
            wraped_model = interaction_response
        else:
            wraped_model = RootInteractionResponse(data=interaction_response)

        if isinstance(interaction_response, INTERACTIONS_CAN_CONTAIN_FILES):
            payload = make_attachment_payload(interaction_response, wraped_model)
        else:
            payload = interaction_response.model_dump(mode='json')

        await self._http_client.post(url=url, payload=payload)

    async def send_pong(
        self,
        interaction_id: SnowflakeInputType,
        interaction_token: str,
    ) -> None:
        """Send a pong response to an interaction.

        It's just a sugar method to send a pong response to an interaction.

        Args:
            interaction_id: Interaction ID.
            interaction_token: Interaction token.
        """
        await self.send_response(
            interaction_id=interaction_id,
            interaction_token=interaction_token,
            interaction_response=InteractionRespPongRequest(),
        )
