"""Contains webhook tests."""

from asyncord.client.webhooks.resources import WebhooksResource
from tests.conftest import IntegrationTestData

# FIXME: Add more tests.


async def test_get_webhooks(
    webhooks_res: WebhooksResource,
    integration_data: IntegrationTestData,
) -> None:
    """Various get webhooks methods."""
    await webhooks_res.get_channel_webhooks(integration_data.channel_id)

    await webhooks_res.get_guild_webhooks(integration_data.guild_id)
