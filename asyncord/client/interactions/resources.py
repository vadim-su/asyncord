"""This module contains resources to perform actions on interactions.

Currently, the only action is to send a response to an interaction. Discord don't
provide any other actions for interactions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from asyncord.client.interactions.models.requests import (
    InteractionRespPongRequest,
    RootInteractionResponse,
)
from asyncord.client.models.attachments import Attachment, make_payload_with_attachments
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
            # Pong response doesn't have a data key, only type
            # It's already as a root model, but without data key
            root_model = interaction_response
        else:
            root_model = RootInteractionResponse(data=interaction_response)

        # if we have any attachments, we need to send them as form
        # Attachment after model mapping is a list of Attachment objects alwayszs or None
        attachments = cast(
            list[Attachment] | None,
            getattr(interaction_response, 'attachments', None),
        )
        payload = make_payload_with_attachments(
            root_model,
            attachments=attachments,
            exclude_unset=False,
            exclude_none=True,
        )

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
