"""Contains webhook tests."""

from asyncord.client.messages.models.requests.embeds import (
    Embed,
)
from asyncord.client.webhooks.models.requests import (
    CreateWebhookRequest,
    ExecuteWebhookRequest,
    UpdateWebhookMessageRequest,
    UpdateWebhookRequest,
)
from asyncord.client.webhooks.resources import WebhooksResource
from tests.conftest import IntegrationTestData

# FIXME: Add more tests.


async def test_webhook_cycle(
    webhooks_res: WebhooksResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test.

    Create webhook.
    Get channel webhooks.
    Get guild webhooks.

    Update webhook.

    Execute webhook(send message).

    Get webhook message.
    Update webhook message.
    Delete webhook message.

    Delete webhook.
    """
    webhook = await webhooks_res.create_webhook(
        integration_data.channel_id,
        create_data=CreateWebhookRequest(
            name='Test Webhook',
            avatar=None,
        ),
    )
    assert webhook
    assert webhook.token

    webhook_channel_resp = await webhooks_res.get_channel_webhooks(
        integration_data.channel_id,
    )

    webhook_guild_resp = await webhooks_res.get_guild_webhooks(
        integration_data.guild_id,
    )

    updated_webhook = await webhooks_res.update_webhook(
        webhook.id,
        update_data=UpdateWebhookRequest(
            name='Updated Test Webhook',
            avatar=None,
        ),
    )

    created_message = await webhooks_res.execute_webhook(
        webhook_id=webhook.id,
        webhook_token=webhook.token,
        execute_data=ExecuteWebhookRequest(
            embeds=[
                Embed(
                    title='Webhook Test',
                    description='This is a test webhook',
                ),
            ],
        ),
        wait=True,
    )

    assert created_message

    message = await webhooks_res.get_webhook_message(
        webhook.id,
        webhook.token,
        created_message.id,
    )

    updated_message = await webhooks_res.update_webhook_message(
        webhook.id,
        webhook.token,
        created_message.id,
        UpdateWebhookMessageRequest(
            embeds=[
                Embed(
                    title='Updated Webhook Test',
                    description='This is an updated test webhook',
                ),
            ],
        ),
    )

    await webhooks_res.delete_webhook_message(webhook.id, webhook.token, created_message.id)
    await webhooks_res.delete_webhook(webhook.id)

    assert message
    assert updated_webhook.name != webhook.name
    assert updated_message
    assert webhook_channel_resp is not None
    assert webhook_guild_resp is not None
