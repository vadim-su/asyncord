import random

import pytest

from asyncord.client.guilds.models.requests import CreateGuildRequest
from asyncord.client.guilds.resources import GuildResource
from asyncord.client.users.resources import UserResource
from tests.conftest import IntegrationTestData


@pytest.mark.parametrize('with_counts', [True, False])
async def test_get_guild(
    guilds_res: GuildResource,
    with_counts: bool,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting a guild."""
    guild = await guilds_res.get(integration_data.guild_id, with_counts=True)
    if with_counts:
        assert guild.approximate_member_count is not None
        assert guild.approximate_presence_count is not None
    assert await guilds_res.get(integration_data.guild_id)


async def test_get_preview(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting a guild preview."""
    assert await guilds_res.get_preview(integration_data.guild_id)


async def test_create_delete_guild(
    guilds_res: GuildResource,
    users_res: UserResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test creating and deleting a guild."""
    suffix = random.randint(0, 1000)
    guild_params = CreateGuildRequest(
        name=f'{integration_data.guild_prefix_to_delete}_{suffix}',
    )
    guild = await guilds_res.create(guild_params)
    assert guild.name.startswith(integration_data.guild_prefix_to_delete)

    all_guilds = await users_res.get_guilds()

    if not any(guild.name.startswith(integration_data.guild_prefix_to_delete) for guild in all_guilds):
        pytest.fail('Guild was not created')

    await guilds_res.delete(guild.id)


async def test_get_prune_count(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the prune count."""
    prune_count = await guilds_res.get_prune_count(integration_data.guild_id)
    assert prune_count.pruned is not None


async def test_get_voice_regions(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the voice regions."""
    assert await guilds_res.get_voice_regions(integration_data.guild_id)


async def test_get_invites(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the invites."""
    invites = await guilds_res.get_invites(integration_data.guild_id)
    assert isinstance(invites, list)
    assert invites


async def test_get_channels(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the channels."""
    assert await guilds_res.get_channels(integration_data.guild_id)


async def test_get_integrations(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the integrations."""
    assert await guilds_res.get_integrations(integration_data.guild_id)

async def test_get_audit_log(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None: 
    """Test getting the audit log."""
    assert await guilds_res.get_audit_log(integration_data.guild_id)