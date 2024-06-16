from asyncord.client.guild_templates.models.requests import (
    CreateGuildTemplateRequest,
    UpdateGuildTemplateRequest,
)
from asyncord.client.guild_templates.resources import GuildTemplatesResource


async def test_guild_template_cycle(guild_templates_res: GuildTemplatesResource) -> None:
    """Test getting a guild template.

    Doesn't test the guild creation from template.
    """
    created_template = await guild_templates_res.create_guild_template(
        CreateGuildTemplateRequest(
            name='test-template',
            description='test template description',
        ),
    )

    assert created_template.name == 'test-template'

    try:
        updated_template = await guild_templates_res.update_guild_template(
            created_template.code,
            UpdateGuildTemplateRequest(
                name='updated-test-template',
                description='updated test template description',
            ),
        )

        requested_template = await guild_templates_res.get_template(
            created_template.code,
        )

        assert requested_template.name == updated_template.name

        templates = await guild_templates_res.get_guild_templates()

        assert templates
    finally:
        await guild_templates_res.delete_guild_template(updated_template.code)
