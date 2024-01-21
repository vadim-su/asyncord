from typing import AsyncGenerator

import aiohttp
import pytest

from asyncord.client.bans.resources import BanResource
from asyncord.client.channels.resources import ChannelResource
from asyncord.client.commands.resources import CommandResource
from asyncord.client.guilds.resources import GuildResource
from asyncord.client.messages.models.requests.messages import CreateMessageRequest
from asyncord.client.messages.models.responses.messages import MessageResponse
from asyncord.client.messages.resources import MessageResource
from asyncord.client.reactions.resources import ReactionResource
from asyncord.client.rest import RestClient
from asyncord.client.roles.resources import RoleResource
from asyncord.client.scheduled_events.resources import ScheduledEventsResource
from asyncord.client.threads.models.common import ThreadType
from asyncord.client.threads.models.requests import CreateThreadRequest
from asyncord.client.threads.models.responses import ThreadResponse
from asyncord.client.threads.resources import ThreadResource
from asyncord.client.users.resources import UserResource
from asyncord.gateway.client import GatewayClient
from tests.conftest import IntegrationTestData


@pytest.fixture()
async def client(token: str) -> RestClient:
    return RestClient(token)


@pytest.fixture()
async def gateway(client: RestClient, token: str) -> AsyncGenerator[GatewayClient, None]:
    async with aiohttp.ClientSession() as session:
        gw = GatewayClient(token, session=session)
        client = RestClient(token)
        client._http_client._session = session  # type: ignore
        gw.dispatcher.add_argument('client', client)
        yield gw


@pytest.fixture()
async def channel_res(client: RestClient) -> ChannelResource:
    return client.channels


@pytest.fixture()
async def messages_res(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> MessageResource:
    return channel_res.messages(integration_data.channel_id)


@pytest.fixture()
async def guilds_res(client: RestClient) -> GuildResource:
    return client.guilds


@pytest.fixture()
async def users_res(client: RestClient) -> UserResource:
    return client.users


@pytest.fixture()
async def members_res(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData
):
    return guilds_res.members(integration_data.guild_id)


@pytest.fixture()
async def roles_res(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> RoleResource:
    return guilds_res.roles(integration_data.guild_id)


@pytest.fixture()
async def events_res(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData
) -> ScheduledEventsResource:
    return guilds_res.events(integration_data.guild_id)


@pytest.fixture()
async def reactions_res(message: MessageResponse, messages_res: MessageResource) -> ReactionResource:
    return messages_res.reactions(message.id)


@pytest.fixture()
async def commands_res(
    client: RestClient,
    integration_data: IntegrationTestData,
) -> CommandResource:
    return client.applications.commands(integration_data.app_id)


@pytest.fixture()
async def thread_res(
    channel_res: ChannelResource,
    integration_data: IntegrationTestData,
) -> ThreadResource:
    return channel_res.threads(integration_data.channel_id)


@pytest.fixture()
async def ban_managment(
    client: RestClient,
    integration_data: IntegrationTestData
) -> BanResource:
    return client.guilds.ban_managment(integration_data.guild_id)


@pytest.fixture()
async def message(messages_res: MessageResource) -> AsyncGenerator[MessageResponse, None]:
    message = await messages_res.create(
        CreateMessageRequest(content='test'),
    )
    yield message
    await messages_res.delete(message.id)


@pytest.fixture()
async def thread(thread_res: ThreadResource) -> AsyncGenerator[ThreadResponse, None]:
    thread = await thread_res.create_thread(
        thread_data=CreateThreadRequest(  # type: ignore
            name='test',
            type=ThreadType.GUILD_PUBLIC_THREAD,
        ),
    )
    yield thread
    await thread_res.delete(thread.id)
