import random

import pytest

from asyncord.client.guilds.models.requests import (
    CreateAutoModerationRuleRequest,
    CreateGuildRequest,
    UpdateWidgetSettingsRequest,
)
from asyncord.client.guilds.resources import GuildResource
from asyncord.client.models.automoderation import (
    AutoModerationRuleEventType,
    RuleAction,
    RuleActionType,
    TriggerMetadata,
    TriggerType,
)
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


async def test_create_get_delete_auto_moderation_rule(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test creating an auto moderation rule."""
    rule = await guilds_res.create_auto_moderation_rule(
        integration_data.guild_id,
        CreateAutoModerationRuleRequest(
            name='Test Rule',
            event_type=AutoModerationRuleEventType.MESSAGE_SEND,
            trigger_type=TriggerType.KEYWORD,
            trigger_metadata=TriggerMetadata(
                keyword_filter=['A very bad word'],
            ),
            actions=[
                RuleAction(
                    type=RuleActionType.BLOCK_MESSAGE,
                ),
            ],
            enabled=True,
        ),
    )

    assert rule

    rule_response = await guilds_res.get_auto_moderation_rule(
        integration_data.guild_id,
        rule.id,
    )

    assert rule.name == rule_response.name

    await guilds_res.delete_auto_moderation_rule(
        integration_data.guild_id,
        rule.id,
    )


async def test_get_list_auto_moderation_rules(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the auto moderation rules."""
    assert await guilds_res.get_list_auto_moderation_rules(
        integration_data.guild_id,
    )


async def test_get_update_widget(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting and updating the widget."""
    settings = await guilds_res.get_widget_settings(integration_data.guild_id)
    assert settings

    updated_widget_settings = await guilds_res.update_widget(
        integration_data.guild_id,
        widget_data=UpdateWidgetSettingsRequest(
            enabled=True,
        ),
    )

    assert updated_widget_settings.enabled

    widget = await guilds_res.get_widget(integration_data.guild_id)
    assert widget

    widget_bytes = await guilds_res.get_widget_image(integration_data.guild_id)
    assert widget_bytes is not None


async def test_get_onboarding(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting and updating the onboarding."""
    onboarding = await guilds_res.get_onboarding(integration_data.guild_id)
    assert onboarding


@pytest.mark.skip('Requires more rights than test bot has.')
async def test_get_vanity_url(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the vanity url."""
    assert await guilds_res.get_vanity_url(integration_data.guild_id)
