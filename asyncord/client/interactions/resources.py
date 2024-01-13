"""This module contains resources to perform actions on interactions.

Currently, the only action is to send a response to an interaction. Discord don't
provide any other actions for interactions.
"""

from typing import Union

from asyncord.client.interactions.models.requests import (
    InteractionChannelMessageResponsRequest,
    InteractionDeferredChannelMessageResponseRequest,
    InteractionDeferredUpdateMessageResponseRequest,
    InteractionPongResponseRequest,
    InteractionResponseRequestType,
    InteractionUpdateMessageResponseRequest,
)
from asyncord.client.resources import ClientSubresource
from asyncord.typedefs import LikeSnowflake
from asyncord.urls import REST_API_URL

_INTERACTIONS_CAN_CONTAIN_FILES = Union[
    InteractionChannelMessageResponsRequest,
    InteractionDeferredChannelMessageResponseRequest,
    InteractionDeferredUpdateMessageResponseRequest,
    InteractionUpdateMessageResponseRequest,
]


class InteractionResource(ClientSubresource):
    """Resource to perform actions on interactions."""

    interactions_url = REST_API_URL / 'interactions'

    async def send_response(
        self,
        interaction_id: LikeSnowflake,
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
        payload = interaction_response.model_dump(mode='json')

        if isinstance(interaction_response, _INTERACTIONS_CAN_CONTAIN_FILES):
            files = [
                (file.filename, file.content_type, file.content)
                for file in interaction_response.data.files
            ]
        else:
            files = None

        await self._http_client.post(url=url, payload=payload, files=files)

    async def send_pong(self, interaction_id: LikeSnowflake, interaction_token: str) -> None:
        """Send a pong response to an interaction.

        Args:
            interaction_id: Interaction ID.
            interaction_token: Interaction token.
        """
        await self.send_response(
            interaction_id=interaction_id,
            interaction_token=interaction_token,
            interaction_response=InteractionPongResponseRequest(),
        )
