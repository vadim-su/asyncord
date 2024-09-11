from collections.abc import AsyncGenerator

import pytest

from asyncord.client.applications.resources import ApplicationResource
from asyncord.client.bans.resources import BanResource
from asyncord.client.channels.models.requests.creation import (
    CreateAnoncementChannelRequest,
    CreateStageChannelRequest,
    CreateTextChannelRequest,
)
from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.commands.resources import CommandResource
from asyncord.client.emojis.resources import EmojiResource
from asyncord.client.guild_templates.resources import GuildTemplatesResource
from asyncord.client.guilds.resources import GuildResource
from asyncord.client.http.middleware.ratelimit import BackoffRateLimitStrategy
from asyncord.client.invites.resources import InvitesResource
from asyncord.client.members.resources import MemberResource
from asyncord.client.messages.models.requests.messages import CreateMessageRequest
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.messages.resources import MessageResource
from asyncord.client.polls.resources import PollsResource
from asyncord.client.rest import RestClient
from asyncord.client.roles.resources import RoleResource
from asyncord.client.scheduled_events.resources import ScheduledEventsResource
from asyncord.client.stage_instances.resources import StageInstancesResource
from asyncord.client.stickers.resources import StickersResource
from asyncord.client.threads.models.common import ThreadType
from asyncord.client.threads.models.requests import CreateThreadRequest
from asyncord.client.threads.models.responses import ThreadResponse
from asyncord.client.threads.resources import ThreadResource
from asyncord.client.users.resources import UserResource
from asyncord.client.webhooks.models.requests import CreateWebhookRequest
from asyncord.client.webhooks.models.responces import WebhookResponse
from asyncord.client.webhooks.resources import WebhooksResource
from tests.conftest import IntegrationTestData


@pytest.fixture
async def client(token: str) -> RestClient:
    """Get a rest client."""
    return RestClient(
        token,
        ratelimit_strategy=BackoffRateLimitStrategy(
            max_retries=10,
            min_wait_time=2,
            max_wait_time=60,
        ),
    )


@pytest.fixture
async def applications_res(
    client: RestClient,
) -> ApplicationResource:
    """Get applications resource for the client."""
    return client.applications


@pytest.fixture
async def stickers_res(
    client: RestClient,
) -> StickersResource:
    """Get stickers resource for the client."""
    return client.stickers


@pytest.fixture
async def webhooks_res(
    client: RestClient,
) -> WebhooksResource:
    """Get webhooks resource for the client."""
    return client.webhooks


@pytest.fixture
async def stage_instances_res(
    client: RestClient,
) -> StageInstancesResource:
    """Get stage instances resource for the client."""
    return client.stage_instances


@pytest.fixture
async def channel_res(client: RestClient) -> ChannelResource:
    """Get channels resource for the client."""
    return client.channels


@pytest.fixture
async def messages_res(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> MessageResource:
    """Get messages resource for the channel."""
    return channel_res.messages(integration_data.channel_id)


@pytest.fixture
async def polls_res(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> PollsResource:
    """Get polls resource for the channel."""
    return channel_res.polls(integration_data.channel_id)


@pytest.fixture
async def guilds_res(client: RestClient) -> GuildResource:
    """Get guilds resource for the client."""
    return client.guilds


@pytest.fixture
async def invite_res(client: RestClient) -> InvitesResource:
    """Get invites resource for the client."""
    return client.invites


@pytest.fixture
async def users_res(client: RestClient) -> UserResource:
    """Get users resource for the client."""
    return client.users


@pytest.fixture
async def members_res(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> MemberResource:
    """Get members resource for the guild."""
    return guilds_res.members(integration_data.guild_id)


@pytest.fixture
async def guild_templates_res(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> GuildTemplatesResource:
    """Get guild templates resource for the guild."""
    return guilds_res.guild_templates(integration_data.guild_id)


@pytest.fixture
async def roles_res(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> RoleResource:
    """Get roles resource for the guild."""
    return guilds_res.roles(integration_data.guild_id)


@pytest.fixture
async def emoji_res(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> EmojiResource:
    """Get emoji resource for the guild."""
    return guilds_res.emojis(integration_data.guild_id)


@pytest.fixture
async def events_res(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> ScheduledEventsResource:
    """Get events resource for the guild."""
    return guilds_res.events(integration_data.guild_id)


@pytest.fixture
async def commands_res(
    client: RestClient,
    integration_data: IntegrationTestData,
) -> CommandResource:
    """Get commands resource for the application."""
    return client.applications.commands(integration_data.app_id)


@pytest.fixture
async def thread_res(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> ThreadResource:
    """Get threads resource for the channel."""
    return channel_res.threads(integration_data.channel_id)


@pytest.fixture
async def ban_managment(
    client: RestClient,
    integration_data: IntegrationTestData,
) -> BanResource:
    """Get ban management resource for the guild."""
    return client.guilds.ban_managment(integration_data.guild_id)


@pytest.fixture
async def message(messages_res: MessageResource) -> AsyncGenerator[MessageResponse, None]:
    """Fixture that creates a message and deletes it after the test."""
    message = await messages_res.create(
        CreateMessageRequest(content='test'),
    )
    yield message
    await messages_res.delete(message.id)


@pytest.fixture
async def thread(thread_res: ThreadResource) -> AsyncGenerator[ThreadResponse, None]:
    """Fixture that creates a thread and deletes it after the test."""
    thread = await thread_res.create_thread(
        thread_data=CreateThreadRequest(  # type: ignore
            name='test',
            type=ThreadType.GUILD_PUBLIC_THREAD,
        ),
    )
    yield thread
    await thread_res.delete(thread.id)


@pytest.fixture
async def channel(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> AsyncGenerator[ChannelResponse, None]:
    """Fixture for creating channel and deleting it after test."""
    channel = await channel_res.create_channel(
        guild_id=integration_data.guild_id,
        channel_data=CreateTextChannelRequest(name='test-channel'),
    )

    yield channel
    await channel_res.delete(channel.id)


@pytest.fixture
async def stage_channel(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> AsyncGenerator[ChannelResponse, None]:
    """Fixture for creating channel and deleting it after test."""
    channel = await channel_res.create_channel(
        integration_data.guild_id,
        CreateStageChannelRequest(name='Test stage channel'),
    )
    yield channel
    await channel_res.delete(channel.id)


@pytest.fixture
async def announcement_channel(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> AsyncGenerator[ChannelResponse, None]:
    """Get the announcement channel."""
    channel = await channel_res.create_channel(
        guild_id=integration_data.guild_id,
        channel_data=CreateAnoncementChannelRequest(name='test-announcement'),
    )

    yield channel

    await channel_res.delete(channel.id)


@pytest.fixture(scope='module')
async def module_client(token: str) -> RestClient:
    """Get new rest client."""
    return RestClient(
        token,
        ratelimit_strategy=BackoffRateLimitStrategy(
            max_retries=10,
            min_wait_time=2,
            max_wait_time=60,
        ),
    )


@pytest.fixture(scope='module')
async def webhook(
    module_client: RestClient,
    integration_data: IntegrationTestData,
) -> AsyncGenerator[WebhookResponse, None]:
    """Get new webhook for module."""
    webhook = await module_client.webhooks.create_webhook(
        integration_data.channel_id,
        CreateWebhookRequest(name='Test Webhook'),
    )

    yield webhook

    await module_client.webhooks.delete_webhook(webhook.id)
