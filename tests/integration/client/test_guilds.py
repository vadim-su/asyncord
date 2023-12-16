import pytest

from asyncord.client.guilds import GuildResource
from asyncord.client.models.guilds import CreateGuildData
from asyncord.client.rest import RestClient
from tests.conftest import IntegrationData


class TestGuilds:
    @pytest.fixture()
    async def guilds(self, client: RestClient):
        yield client.guilds

    @pytest.mark.parametrize('with_counts', [True, False])
    async def test_get_guild(
        self,
        guilds: GuildResource,
        with_counts: bool,
        integration_data: IntegrationData
    ):
        guild = await guilds.get(integration_data.TEST_GUILD_ID, with_counts=True)
        if with_counts:
            assert guild.approximate_member_count is not None
            assert guild.approximate_presence_count is not None
        assert await guilds.get(integration_data.TEST_GUILD_ID)

    async def test_get_preview(
        self,
        guilds: GuildResource,
        integration_data: IntegrationData
    ):
        assert await guilds.get_preview(integration_data.TEST_GUILD_ID)

    async def test_create_guild(
        self,
        guilds: GuildResource,
        integration_data: IntegrationData
    ):
        guild_params = CreateGuildData(
            name=integration_data.TEST_GUILD_NAME,
        )
        guild = await guilds.create(guild_params)
        assert guild.name == integration_data.TEST_GUILD_NAME

    async def test_delete(
        self,
        client: RestClient,
        guilds: GuildResource,
        integration_data: IntegrationData
    ):
        for guild in await client.users.get_guilds():
            if guild.name == integration_data.TEST_GUILD_NAME:
                await guilds.delete(guild.id)

    async def test_get_prune_count(
        self,
        guilds: GuildResource,
        integration_data: IntegrationData
    ):
        prune_count = await guilds.get_prune_count(integration_data.TEST_GUILD_ID)
        assert prune_count.pruned is not None

    async def test_get_voice_regions(
        self,
        guilds: GuildResource,
        integration_data: IntegrationData
    ):
        assert await guilds.get_voice_regions(integration_data.TEST_GUILD_ID)

    async def test_get_invites(
        self,
        guilds: GuildResource,
        integration_data: IntegrationData
    ):
        invites = await guilds.get_invites(integration_data.TEST_GUILD_ID)
        assert isinstance(invites, list)
        assert invites

    async def test_get_channels(
        self,
        guilds: GuildResource,
        integration_data: IntegrationData
    ):
        assert await guilds.get_channels(integration_data.TEST_GUILD_ID)

    async def test_get_integrations(
        self,
        guilds: GuildResource,
        integration_data: IntegrationData
    ):
        assert await guilds.get_integrations(integration_data.TEST_GUILD_ID)
