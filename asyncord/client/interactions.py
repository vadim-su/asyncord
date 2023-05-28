from asyncord.client.models.interactions import InteractionResponseData, InteractionResponseType
from asyncord.client.resources import ClientSubresources
from asyncord.typedefs import LikeSnowflake
from asyncord.urls import REST_API_URL


class InteractionResource(ClientSubresources):
    """Resource to perform actions on interactions."""

    async def send_response(self, interaction_id: LikeSnowflake, interaction_token: str, response: InteractionResponseData) -> None:
        """Send a response to an interaction.

        Args:
            interaction_id (int): interaction ID.
            interaction_token (str): Interaction token.
            response (InteractionResponseData): Response to send.
        """
        url = REST_API_URL / 'interactions' / str(interaction_id) / interaction_token / 'callback'
        payload = response.model_dump(mode='json')
        await self._http.post(url, payload)

    async def send_pong(self, interaction_id: LikeSnowflake, interaction_token: str) -> None:
        """Send a pong response to an interaction.

        Args:
            interaction_id (int): interaction ID.
            interaction_token (str): Interaction token.
        """
        await self.send_response(
            interaction_id=interaction_id,
            interaction_token=interaction_token,
            response=InteractionResponseData(type=InteractionResponseType.PONG),
        )
