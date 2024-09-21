from collections.abc import AsyncGenerator

import pytest

from asyncord.client.guild_templates.models.requests import (
    CreateGuildFromTemplateRequest,
    CreateGuildTemplateRequest,
    UpdateGuildTemplateRequest,
)
from asyncord.client.guild_templates.models.responses import GuildTemplateResponse
from asyncord.client.guild_templates.resources import GuildTemplatesResource
from asyncord.client.guilds.resources import GuildResource


@pytest.fixture
async def guild_templates(
    guild_templates_res: GuildTemplatesResource,
) -> AsyncGenerator[GuildTemplateResponse, None]:
    """Create a guild template and delete it after the test."""
    template = await guild_templates_res.create_guild_template(
        CreateGuildTemplateRequest(
            name='TestTemplate',
            description='Test template description',
        ),
    )
    yield template
    await guild_templates_res.delete_guild_template(template.code)


async def test_get_template(
    guild_templates: GuildTemplateResponse,
    guild_templates_res: GuildTemplatesResource,
) -> None:
    """Test getting a guild template."""
    retrieved_template = await guild_templates_res.get_template(guild_templates.code)
    assert retrieved_template.name == 'TestTemplate'


async def test_update_template(
    guild_templates: GuildTemplateResponse,
    guild_templates_res: GuildTemplatesResource,
) -> None:
    """Test updating a guild template."""
    updated_template = await guild_templates_res.update_guild_template(
        guild_templates.code,
        UpdateGuildTemplateRequest(
            name='UpdatedTemplate',
            description='Updated template description',
        ),
    )
    assert updated_template.name == 'UpdatedTemplate'


async def test_sync_template(
    guild_templates: GuildTemplateResponse,
    guild_templates_res: GuildTemplatesResource,
) -> None:
    """Test syncing a guild template."""
    assert await guild_templates_res.sync_guild_template(guild_templates.code)


async def test_create_guild_from_template(
    guild_templates: GuildTemplateResponse,
    guild_templates_res: GuildTemplatesResource,
    guilds_res: GuildResource,
) -> None:
    """Test creating a guild from a template."""
    guild = await guild_templates_res.create_guild_from_template(
        guild_templates.code,
        CreateGuildFromTemplateRequest(name='TestGuild'),
    )

    try:
        assert guild.owner_id == guild_templates.creator_id
    finally:
        await guilds_res.delete(guild.id)
