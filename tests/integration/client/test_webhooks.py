import pytest

from asyncord.client.http.errors import NotFoundError
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.rest import RestClient
from asyncord.client.webhooks.models.requests import (
    ExecuteWebhookRequest,
    UpdateWebhookMessageRequest,
    UpdateWebhookRequest,
)
from asyncord.client.webhooks.models.responces import WebhookResponse
from asyncord.client.webhooks.resources import WebhooksResource
from tests.conftest import IntegrationTestData


@pytest.fixture(scope='module')
async def module_webhook_res(module_client: RestClient) -> WebhooksResource:
    """Get webhooks resource for the module."""
    return module_client.webhooks


@pytest.fixture(scope='module')
async def webhook_message(
    webhook: WebhookResponse,
    module_webhook_res: WebhooksResource,
) -> MessageResponse:
    """Create a webhook message."""
    return await module_webhook_res.execute_webhook(
        webhook_id=webhook.id,
        token=webhook.token,  # type: ignore
        execution_data=ExecuteWebhookRequest(content='Hello World'),
    )


async def test_get_channel_webhooks(
    webhooks_res: WebhooksResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting all webhooks in a channel."""
    webhooks = await webhooks_res.get_channel_webhooks(integration_data.channel_id)
    assert isinstance(webhooks, list)


async def test_get_guild_webhooks(
    webhooks_res: WebhooksResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting all webhooks in a guild."""
    webhooks = await webhooks_res.get_guild_webhooks(integration_data.guild_id)
    assert isinstance(webhooks, list)


@pytest.mark.parametrize('with_token', [False, True])
async def test_get_webhook(
    with_token: bool,
    webhooks_res: WebhooksResource,
    webhook: WebhookResponse,
) -> None:
    """Test getting a webhook by its id."""
    if with_token:
        token = webhook.token  # type: ignore
    else:
        token = None
    new_webhook_obj = await webhooks_res.get_webhook(webhook.id, token=token)
    assert new_webhook_obj.id == webhook.id


async def test_update_with_token_and_channel_forbidden(webhooks_res: WebhooksResource) -> None:
    """Test updating a webhook with token and channel_id."""
    with pytest.raises(ValueError, match='`channel_id` cannot be set'):
        await webhooks_res.update_webhook(
            webhook_id='webhook_id',
            update_data=UpdateWebhookRequest(name='Updated Webhook', channel_id=123),
            token='token',  # noqa: S106
        )


async def test_update_webhook(
    webhook: WebhookResponse,
    module_webhook_res: WebhooksResource,
) -> None:
    """Test updating a webhook."""
    update_data = UpdateWebhookRequest(name='Updated Webhook')
    webhook = await module_webhook_res.update_webhook(
        webhook_id=webhook.id,
        update_data=update_data,
    )
    assert webhook.name == 'Updated Webhook'


@pytest.mark.parametrize(
    'wait',
    [False, True],
)
async def test_execute_webhook(
    wait: bool,
    webhook: WebhookResponse,
    module_webhook_res: WebhooksResource,
) -> None:
    """Test executing a webhook."""
    message = await module_webhook_res.execute_webhook(
        webhook_id=webhook.id,
        token=webhook.token,  # type: ignore
        execution_data=ExecuteWebhookRequest(content='Hello World'),
        wait=wait,
    )
    assert bool(message) is wait

    if not message:
        return

    assert message.content == 'Hello World'


async def test_get_webhook_message(
    webhook_message: MessageResponse,
    webhook: WebhookResponse,
    module_webhook_res: WebhooksResource,
) -> None:
    """Test getting a webhook message."""
    token: str = webhook.token  # type: ignore
    retrieved_message = await module_webhook_res.get_webhook_message(
        webhook_id=webhook.id,
        token=token,
        message_id=webhook_message.id,
    )
    assert webhook_message.id == retrieved_message.id


async def test_update_webhook_message(
    webhook_message: MessageResponse,
    webhook: WebhookResponse,
    module_webhook_res: WebhooksResource,
) -> None:
    """Test updating a webhook message."""
    token: str = webhook.token  # type: ignore
    updated_message = await module_webhook_res.update_webhook_message(
        webhook_id=webhook.id,
        token=token,
        message_id=webhook_message.id,
        update_data=UpdateWebhookMessageRequest(content='updated'),
    )
    assert updated_message.content == 'updated'


async def test_delete_webhook_message(
    webhook_message: MessageResponse,
    webhook: WebhookResponse,
    module_webhook_res: WebhooksResource,
) -> None:
    """Test deleting a webhook message."""
    token: str = webhook.token  # type: ignore

    await module_webhook_res.delete_webhook_message(
        webhook_id=webhook.id,
        token=token,
        message_id=webhook_message.id,
    )
    # Assert deletion by trying to fetch the deleted message
    with pytest.raises(NotFoundError):
        await module_webhook_res.get_webhook_message(
            webhook_id=webhook.id,
            token=token,
            message_id=webhook_message.id,
        )
