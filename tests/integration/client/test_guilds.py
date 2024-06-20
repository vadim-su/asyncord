import random

import pytest

from asyncord.client.guilds.models.common import MFALevel, OnboardingMode, OnboardingPromptType, WidgetStyleOptions
from asyncord.client.guilds.models.requests import (
    CreateAutoModerationRuleRequest,
    CreateGuildRequest,
    OnboardingPrompt,
    OnboardingPromptOption,
    UpdateOnboardingRequest,
    UpdateWelcomeScreenRequest,
    UpdateWidgetSettingsRequest,
)
from asyncord.client.guilds.resources import GuildResource
from asyncord.client.http import errors
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
    updated_widget_settings = await guilds_res.update_widget(
        integration_data.guild_id,
        widget_data=UpdateWidgetSettingsRequest(
            enabled=True,
        ),
    )
    assert updated_widget_settings.enabled


async def test_get_widget(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the widget."""
    widget = await guilds_res.get_widget(integration_data.guild_id)
    assert widget.id == integration_data.guild_id


@pytest.mark.parametrize('style', [None] + [style for style in WidgetStyleOptions])
async def test_get_widget_image(
    style: WidgetStyleOptions | None,
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the widget image."""
    widget_image = await guilds_res.get_widget_image(
        integration_data.guild_id,
        style=style,
    )
    assert widget_image.image_data.startswith('data:')


async def test_get_onboarding(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting and updating the onboarding."""
    assert await guilds_res.get_onboarding(integration_data.guild_id)


async def test_update_onboarding(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test updating the onboarding."""
    onboarding = await guilds_res.update_onboarding(
        integration_data.guild_id,
        UpdateOnboardingRequest(
            prompts=[
                OnboardingPrompt(
                    type=OnboardingPromptType.DROPDOWN,
                    title='Select a channel to get started!',
                    options=[
                        OnboardingPromptOption(
                            channel_ids=[integration_data.channel_id],
                            title='Welcome to the server!',
                        ),
                    ],
                    single_select=False,
                    required=True,
                    in_onboarding=True,
                ),
                OnboardingPrompt(
                    type=OnboardingPromptType.DROPDOWN,
                    title='Select a channel to get started 2!',
                    options=[
                        OnboardingPromptOption(
                            role_ids={integration_data.role_id},
                            title='Welcome to the server 2!',
                        ),
                    ],
                    single_select=False,
                ),
            ],
            default_channel_ids=[],
            enabled=False,
            mode=OnboardingMode.ONBOARDING_DEFAULT,
        ),
    )
    assert onboarding.enabled is False
    assert onboarding.mode == OnboardingMode.ONBOARDING_DEFAULT
    assert len(onboarding.prompts) == 2
    assert onboarding.prompts[0].id

    onboarding = await guilds_res.update_onboarding(
        integration_data.guild_id,
        UpdateOnboardingRequest(
            prompts=[],
            default_channel_ids=[],
        ),
    )
    assert not onboarding.prompts
    assert not onboarding.default_channel_ids


async def test_welcome_screen_management(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test updating and getting welcome screen."""
    assert await guilds_res.update_welcome_screen(
        integration_data.guild_id,
        UpdateWelcomeScreenRequest(
            enabled=True,
            description='Welcome to the server!',
        ),
    )
    assert await guilds_res.get_welcome_screen(integration_data.guild_id)

    assert await guilds_res.update_welcome_screen(
        integration_data.guild_id,
        UpdateWelcomeScreenRequest(
            enabled=False,
            description=None,
        ),
    )


async def test_update_mfa_level(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test updating the MFA level.

    We just check that method and input in general valid. Bot has no enough
    permissions to update MFA level.
    """
    with pytest.raises(errors.ClientError, match='Missing Access'):
        await guilds_res.update_mfa(
            integration_data.guild_id,
            level=MFALevel.NONE,
        )


async def test_delete_integration(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test deleting an integration."""
    with pytest.raises(errors.ClientError, match='Unknown Integration'):
        assert await guilds_res.delete_integration(
            integration_data.guild_id,
            '34124324134',
        )


async def test_get_vanity_url(
    guilds_res: GuildResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test getting the vanity url.

    We just check that method and input in general valid. Bot has no enough
    permissions to get vanity url.
    """
    with pytest.raises(errors.ClientError, match='Missing Access'):
        assert await guilds_res.get_vanity_url(integration_data.guild_id)
