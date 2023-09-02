"""This module contains resources to perform actions on interactions.

Currently, the only action is to send a response to an interaction. Discord don't
provide any other actions for interactions.
"""

from asyncord.client.models.interactions import (
    InteractionDeferredUpdateMessageResponseData,
    InteractionPongResponseData,
    InteractionResponse,
    InteractionUpdateMessageResponseData,
    IteractionChannelMessageResponseData,
    IteractionDeferredChannelMessageResponseData,
)
from asyncord.client.resources import ClientSubresources
from asyncord.typedefs import LikeSnowflake
from asyncord.urls import REST_API_URL

_INTERACTIONS_CAN_CONTAIN_FILES = (
    IteractionChannelMessageResponseData
    | IteractionDeferredChannelMessageResponseData
    | InteractionDeferredUpdateMessageResponseData
    | InteractionUpdateMessageResponseData
)


class InteractionResource(ClientSubresources):
    """Resource to perform actions on interactions."""

    interactions_url = REST_API_URL / 'interactions'

    async def send_response(
        self,
        interaction_id: LikeSnowflake,
        interaction_token: str,
        interaction_response: InteractionResponse,
    ) -> None:
        """Send a response to an interaction.

        Args:
            interaction_id (int): interaction ID.
            interaction_token (str): Interaction token.
            interaction_response (InteractionResponse): Response to send to the interaction.
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

        await self._http.post(url=url, payload=payload, files=files)

    async def send_pong(self, interaction_id: LikeSnowflake, interaction_token: str) -> None:
        """Send a pong response to an interaction.

        Args:
            interaction_id (int): interaction ID.
            interaction_token (str): Interaction token.
        """
        await self.send_response(
            interaction_id=interaction_id,
            interaction_token=interaction_token,
            interaction_response=InteractionPongResponseData(),
        )
