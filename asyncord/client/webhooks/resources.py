"""This module contains the WebhooksResource class.

Reference:
https://discord.com/developers/docs/resources/webhook
"""

from __future__ import annotations

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.resources import ClientSubresource
from asyncord.client.webhooks.models.requests import (
    CreateWebhookRequest,
    ExecuteWebhookRequest,
    UpdateWebhookMessageRequest,
    UpdateWebhookRequest,
)
from asyncord.client.webhooks.models.responces import (
    WebhookResponse,
)
from asyncord.snowflake import SnowflakeInputType
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL


class WebhooksResource(ClientSubresource):
    """Webhooks resource.

    Attributes:
        guilds_url: guilds url.
        channel_url: channels url.
        webhooks_url: Webhooks url.
    """

    guilds_url = REST_API_URL / 'guilds'
    channel_url = REST_API_URL / 'channels'
    webhooks_url = REST_API_URL / 'webhooks'

    async def get_channel_webhooks(
        self,
        channel_id: SnowflakeInputType,
    ) -> list[WebhookResponse]:
        """Returns lists of channel webhooks.

        Reference:
        https://discord.com/developers/docs/resources/webhook#get-channel-webhooks

        Args:
            channel_id: ID of the channel to get webhooks for.
        """
        url = self.channel_url / str(channel_id) / 'webhooks'
        resp = await self._http_client.get(url)
        return list_model(WebhookResponse).validate_python(resp.body)

    async def get_guild_webhooks(
        self,
        guild_id: SnowflakeInputType,
    ) -> list[WebhookResponse]:
        """Returns lists of guild webhooks.

        Reference:
        https://discord.com/developers/docs/resources/webhook#get-guild-webhooks

        Args:
            guild_id: ID of the guild to get webhooks for.
        """
        url = self.guilds_url / str(guild_id) / 'webhooks'
        resp = await self._http_client.get(url)
        return list_model(WebhookResponse).validate_python(resp.body)

    async def get_webhook(
        self,
        webhook_id: SnowflakeInputType,
        webhook_token: str | None = None,
    ) -> WebhookResponse:
        """Returns a new webhook object.

        Reference:
        https://discord.com/developers/docs/resources/webhook#get-webhook

        Args:
            webhook_id: ID of the webhook to get.
            webhook_token: Token of the webhook.
        """
        url = self.webhooks_url / str(webhook_id)

        if webhook_token is not None:
            url /= str(webhook_token)

        resp = await self._http_client.get(url)
        return WebhookResponse.model_validate(resp.body)

    async def create_webhook(
        self,
        channel_id: SnowflakeInputType,
        create_data: CreateWebhookRequest,
        reason: str | None = None,
    ) -> WebhookResponse:
        """Create a new webhook.

        Reference:
        https://discord.com/developers/docs/resources/webhook#create-webhook

        Args:
            channel_id: ID of the channel to create the webhook in.
            create_data: Webhook data.
            reason: Reason for creating the webhook.
        """
        url = self.channel_url / str(channel_id) / 'webhooks'

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = create_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url, payload, headers=headers)
        return WebhookResponse.model_validate(resp.body)

    async def update_webhook(
        self,
        webhook_id: SnowflakeInputType,
        update_data: UpdateWebhookRequest,
        webhook_token: str | None = None,
        reason: str | None = None,
    ) -> WebhookResponse:
        """Modify a webhook with a token.

        Reference:
        https://discord.com/developers/docs/resources/webhook#modify-webhook
        https://discord.com/developers/docs/resources/webhook#modify-webhook-with-token

        Args:
            webhook_id: ID of the webhook to modify.
            update_data: Webhook data.
            webhook_token: Token of the webhook.
            reason: Reason for updating the webhook.
        """
        url = self.webhooks_url / str(webhook_id)

        payload = update_data.model_dump(mode='json', exclude_unset=True)

        if webhook_token is not None:
            url /= str(webhook_token)
            if 'channel_id' in payload:
                del payload['channel_id']

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        resp = await self._http_client.patch(url, payload, headers=headers)
        return WebhookResponse.model_validate(resp.body)

    async def delete_webhook(
        self,
        webhook_id: SnowflakeInputType,
        webhook_token: str | None = None,
        reason: str | None = None,
    ) -> None:
        """Delete a webhook.

        Reference:
        https://discord.com/developers/docs/resources/webhook#delete-webhook
        https://discord.com/developers/docs/resources/webhook#delete-webhook-with-token

        Args:
            webhook_id: ID of the webhook to delete.
            webhook_token: Token of the webhook.
            reason: Reason for deleting the webhook.
        """
        url = self.webhooks_url / str(webhook_id)
        if webhook_token is not None:
            url /= str(webhook_token)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url, headers=headers)

    async def execute_webhook(  # noqa: PLR0913
        self,
        webhook_id: SnowflakeInputType,
        webhook_token: str,
        execute_data: ExecuteWebhookRequest,
        wait: bool | None = None,
        thread_id: SnowflakeInputType | None = None,
    ) -> None:
        """Execute a webhook.

        Reference:
        https://discord.com/developers/docs/resources/webhook#execute-webhook

        Args:
            webhook_id: ID of the webhook to execute.
            webhook_token: Token of the webhook.
            execute_data: Webhook data.
            wait: Waits for server confirmation.
            thread_id: Send the message to the specified thread.
        """
        params = {}
        if wait is not None:
            params['wait'] = wait
        if thread_id is not None:
            params['thread_id'] = thread_id

        url = self.webhooks_url / str(webhook_id) / str(webhook_token) % params
        payload = execute_data.model_dump(mode='json', exclude_unset=True)
        await self._http_client.post(
            url,
            payload,
            files=[(file.filename, file.content_type, file.content) for file in execute_data.files],
        )

    async def get_webhook_message(
        self,
        webhook_id: SnowflakeInputType,
        webhook_token: str,
        message_id: SnowflakeInputType,
        thread_id: SnowflakeInputType | None = None,
    ) -> MessageResponse:
        """Returns a previously-sent webhook message.

        Reference:
        https://discord.com/developers/docs/resources/webhook#get-webhook-message

        Args:
            webhook_id: ID of the webhook.
            webhook_token: Token of the webhook.
            message_id: ID of the message.
            thread_id: ID of the thread.
        """
        url = self.webhooks_url / str(webhook_id) / str(webhook_token) / 'messages' / str(message_id)
        if thread_id is not None:
            params = {'thread_id': thread_id}
            url %= params

        resp = await self._http_client.get(url)
        return MessageResponse.model_validate(resp.body)

    async def update_webhook_message(  # noqa: PLR0913
        self,
        webhook_id: SnowflakeInputType,
        webhook_token: str,
        message_id: SnowflakeInputType,
        update_data: UpdateWebhookMessageRequest,
        thread_id: SnowflakeInputType | None = None,
    ) -> MessageResponse:
        """Edit a previously-sent webhook message.

        Reference:
        https://discord.com/developers/docs/resources/webhook#edit-webhook-message

        Args:
            webhook_id: ID of the webhook.
            webhook_token: Token of the webhook.
            message_id: ID of the message.
            update_data: Message data.
            thread_id: ID of the thread.
        """
        url = self.webhooks_url / str(webhook_id) / str(webhook_token) / 'messages' / str(message_id)
        if thread_id is not None:
            params = {'thread_id': thread_id}
            url %= params

        payload = update_data.model_dump(mode='json', exclude_unset=True)

        resp = await self._http_client.patch(
            url,
            payload,
            files=[(file.filename, file.content_type, file.content) for file in update_data.files],
        )

        return MessageResponse.model_validate(resp.body)

    async def delete_webhook_message(
        self,
        webhook_id: SnowflakeInputType,
        webhook_token: str,
        message_id: SnowflakeInputType,
        thread_id: SnowflakeInputType | None = None,
    ) -> None:
        """Delete a previously-sent webhook message.

        Reference:
        https://discord.com/developers/docs/resources/webhook#delete-webhook-message

        Args:
            webhook_id: ID of the webhook.
            webhook_token: Token of the webhook.
            message_id: ID of the message.
            thread_id: ID of the thread.
        """
        url = self.webhooks_url / str(webhook_id) / str(webhook_token) / 'messages' / str(message_id)
        if thread_id is not None:
            params = {'thread_id': thread_id}
            url %= params

        await self._http_client.delete(url)
