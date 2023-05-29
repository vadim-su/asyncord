import pytest

from asyncord.client.rest import RestClient
from asyncord.client.guilds import GuildResource
from asyncord.client.models.guilds import CreateGuildData

TEST_GUILD_NAME = 'TestGuild'
TEST_GUILD_ID = '763522265874694144'


class TestGuilds:
    @pytest.fixture()
    async def guilds(self, client: RestClient):
        yield client.guilds

    async def test_get_preview(self, guilds: GuildResource):
        assert await guilds.get_preview(TEST_GUILD_ID)

    async def test_craete_guild(self, guilds: GuildResource):
        guild_params = CreateGuildData(
            name=TEST_GUILD_NAME,
        )
        guild = await guilds.create(guild_params)
        assert guild.name == TEST_GUILD_NAME

    async def test_delete(self, client: RestClient, guilds: GuildResource):
        for guild in await client.users.get_guilds():
            if guild.name == TEST_GUILD_NAME:
                await guilds.delete(guild.id)

    async def test_get_prune_count(self, guilds: GuildResource):
        prune_count = await guilds.get_prune_count(TEST_GUILD_ID)
        assert prune_count.pruned is not None

    async def test_get_voice_regions(self, guilds: GuildResource):
        assert await guilds.get_voice_regions(TEST_GUILD_ID)

    async def test_get_invites(self, guilds: GuildResource):
        invites = await guilds.get_invites(TEST_GUILD_ID)
        assert isinstance(invites, list)
        assert invites

    async def test_get_channels(self, guilds: GuildResource):
        assert await guilds.get_channels(TEST_GUILD_ID)

    async def test_get_integrations(self, guilds: GuildResource):
        assert await guilds.get_integrations(TEST_GUILD_ID)
