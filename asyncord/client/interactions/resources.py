"""This module contains resources to perform actions on interactions.

Currently, the only action is to send a response to an interaction. Discord don't
provide any other actions for interactions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, cast

from asyncord.client.interactions.models.requests import (
    InteractionRespPongRequest,
    RootInteractionResponse,
)
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.models.attachments import Attachment, make_payload_with_attachments
from asyncord.client.resources import APIResource
from asyncord.client.webhooks.models.requests import UpdateWebhookMessageRequest
from asyncord.snowflake import SnowflakeInputType
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.interactions.models.requests import InteractionResponseRequestType
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('InteractionResource',)


class InteractionResource(APIResource):
    """Resource to perform actions on interactions.

    This resource uses two way to interact with interactions - Interaction URL
    and Webhook URL. So it looks weird, but we need to use webhook model to modify
    the interaction response.
    """

    interactions_url = REST_API_URL / 'interactions'
    """URL to interact with interactions."""

    webhook_url = REST_API_URL / 'webhooks'
    """URL to interact with webhooks.

    It's used to get, update, delete the interaction response.
    """

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

    async def get_original_response(
        self,
        application_id: SnowflakeInputType,
        interaction_token: str,
    ) -> MessageResponse:
        """Get the original interaction response.

        It's used to get the response that was sent to the interaction.

        Args:
            application_id: Application ID.
            interaction_token: Interaction token.

        Returns:
            Original interaction response.
        """
        return await self.get_response(
            application_id=application_id,
            interaction_token=interaction_token,
            message_id='@original',
        )

    async def get_response(
        self,
        application_id: SnowflakeInputType,
        interaction_token: str,
        message_id: SnowflakeInputType | Literal['@original'],
    ) -> MessageResponse:
        """Get an interaction response.

        Args:
            application_id: Application ID.
            interaction_token: Interaction token.
            message_id: Message ID.

        Returns:
            Interaction response message.
        """
        url = self.webhook_url / str(application_id) / interaction_token / 'messages' / str(message_id)
        response = await self._http_client.get(url=url)
        return MessageResponse.model_validate(response.body)

    async def update_original_response(
        self,
        application_id: SnowflakeInputType,
        interaction_token: str,
        update_data: UpdateWebhookMessageRequest,
    ) -> MessageResponse:
        """Update the original interaction response.

        Args:
            application_id: Application ID.
            interaction_token: Interaction token.
            update_data: Data to update the interaction response.

        Returns:
            Updated interaction response message.
        """
        return await self.update_response(
            application_id=application_id,
            interaction_token=interaction_token,
            message_id='@original',
            update_data=update_data,
        )

    async def update_response(
        self,
        application_id: SnowflakeInputType,
        interaction_token: str,
        message_id: SnowflakeInputType | Literal['@original'],
        update_data: UpdateWebhookMessageRequest,
    ) -> MessageResponse:
        """Update an interaction response.

        Args:
            application_id: Application ID.
            interaction_token: Interaction token.
            message_id: Message ID.
            update_data: Data to update the interaction response.

        Returns:
            Updated interaction response message.
        """
        url = self.webhook_url / str(application_id) / interaction_token / 'messages' / str(message_id)

        attachments = cast(list[Attachment] | None, update_data.attachments)
        payload = make_payload_with_attachments(update_data, attachments=attachments)
        response = await self._http_client.patch(url=url, payload=payload)
        return MessageResponse.model_validate(response.body)

    async def delete_original_response(
        self,
        application_id: SnowflakeInputType,
        interaction_token: str,
    ) -> None:
        """Delete the original interaction response.

        Args:
            application_id: Application ID.
            interaction_token: Interaction token.
        """
        await self.delete_response(
            application_id=application_id,
            interaction_token=interaction_token,
            message_id='@original',
        )

    async def delete_response(
        self,
        application_id: SnowflakeInputType,
        interaction_token: str,
        message_id: SnowflakeInputType | Literal['@original'],
    ) -> None:
        """Delete an interaction response.

        Args:
            application_id: Application ID.
            interaction_token: Interaction token.
            message_id: Message ID.
        """
        url = self.webhook_url / str(application_id) / interaction_token / 'messages' / str(message_id)
        await self._http_client.delete(url=url)
