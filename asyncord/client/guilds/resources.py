"""This module contains the guilds resource endpoints.

Reference:
https://discord.com/developers/docs/resources/guild
"""

from __future__ import annotations

import datetime
from collections.abc import Sequence
from typing import TYPE_CHECKING

from asyncord.base64_image import Base64Image
from asyncord.client.bans.resources import BanResource
from asyncord.client.channels.models.responses import ChannelResponse
from asyncord.client.emojis.resources import EmojiResource
from asyncord.client.guild_templates.resources import GuildTemplatesResource
from asyncord.client.guilds.models.common import MFALevel
from asyncord.client.guilds.models.responses import (
    AuditLogResponse,
    GuildPreviewResponse,
    GuildResponse,
    IntegrationResponse,
    InviteResponse,
    OnboardingResponse,
    PruneResponse,
    VanityUrlInviteResponse,
    VoiceRegionResponse,
    WelcomeScreenResponse,
    WidgetResponse,
    WidgetSettingsResponse,
)
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.members.resources import MemberResource
from asyncord.client.models.automoderation import AutoModerationRule
from asyncord.client.resources import APIResource
from asyncord.client.roles.resources import RoleResource
from asyncord.client.scheduled_events.resources import ScheduledEventsResource
from asyncord.typedefs import CURRENT_USER, list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    import datetime

    from asyncord.client.guilds.models.common import WidgetStyleOptions
    from asyncord.client.guilds.models.requests import (
        CreateAutoModerationRuleRequest,
        CreateGuildRequest,
        PruneRequest,
        UpdateAutoModerationRuleRequest,
        UpdateOnboardingRequest,
        UpdateWelcomeScreenRequest,
        UpdateWidgetSettingsRequest,
    )
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('GuildResource',)


class GuildResource(APIResource):  # noqa: PLR0904
    """Representaion of the guilds resource.

    Attributes:
        guilds_url: Guilds resource URL.
    """

    guilds_url = REST_API_URL / 'guilds'

    def members(self, guild_id: SnowflakeInputType) -> MemberResource:
        """Get the member subresource for a guild.

        Args:
            guild_id: ID of guild to get the member subresource for.

        Returns:
            Member subresource for the guild.
        """
        return MemberResource(self._http_client, guild_id)

    def guild_templates(self, guild_id: SnowflakeInputType) -> GuildTemplatesResource:
        """Get the guild templates subresource for a guild.

        Args:
            guild_id: ID of the guild to get the guild templates subresource for.
        """
        return GuildTemplatesResource(self._http_client, guild_id)

    def ban_managment(self, guild_id: SnowflakeInputType) -> BanResource:
        """Get the ban subresource for a guild.

        Args:
            guild_id: ID of the guild to get the ban subresource for.

        Returns:
            Ban subresource for the guild.
        """
        return BanResource(self._http_client, guild_id)

    def roles(self, guild_id: SnowflakeInputType) -> RoleResource:
        """Get the role subresource for a guild.

        Args:
            guild_id: ID of the guild to get the role subresource for.

        Returns:
            Role subresource for the guild.
        """
        return RoleResource(self._http_client, guild_id)

    def events(self, guild_id: SnowflakeInputType) -> ScheduledEventsResource:
        """Get the events subresource for a guild.

        Args:
            guild_id: ID of the guild to get the events subresource for.

        Returns:
            Events subresource for the guild.
        """
        return ScheduledEventsResource(self._http_client, guild_id)

    def emojis(self, guild_id: SnowflakeInputType) -> EmojiResource:
        """Get the emojis subresource for a guild.

        Args:
            guild_id: ID of the guild to get the emojis subresource for.

        Returns:
            Emojis subresource for the guild.
        """
        return EmojiResource(self._http_client, guild_id)

    async def get(self, guild_id: SnowflakeInputType, with_counts: bool = False) -> GuildResponse:
        """Get a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#et-guild

        Args:
            guild_id: ID of the guild to get.
            with_counts: Whether to include approximate members.

        Returns:
            Guild with the specified ID.
        """
        url = self.guilds_url / str(guild_id) % {'with_counts': str(with_counts)}
        resp = await self._http_client.get(url=url)
        return GuildResponse.model_validate(resp.body)

    async def get_preview(self, guild_id: SnowflakeInputType) -> GuildPreviewResponse:
        """Get a guild preview.

        Preview guilds are a special type of guilds object that contain only
        the most vital information about a guild.

        Args:
            guild_id: ID of the guild to get the preview for.

        Returns:
            Preview of the guild with the specified ID.
        """
        url = self.guilds_url / str(guild_id) / 'preview'
        resp = await self._http_client.get(url=url)
        return GuildPreviewResponse.model_validate(resp.body)

    async def create(self, guild_data: CreateGuildRequest) -> GuildResponse:
        """Create a new guild.

        This endpoint can be used only by bots in less than 10 guilds.

        Reference:
        https://discord.com/developers/docs/resources/guild#create-guild

        Args:
            guild_data: The data for the guild to create.

        Returns:
            The created guild.
        """
        payload = guild_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url=self.guilds_url, payload=payload)
        return GuildResponse.model_validate(resp.body)

    async def delete(self, guild_id: SnowflakeInputType) -> None:
        """Delete a guild.

        Args:
            guild_id: ID of the guild to delete.
        """
        url = self.guilds_url / str(guild_id)
        await self._http_client.delete(url=url)

    async def update_mfa(self, guild_id: SnowflakeInputType, level: MFALevel) -> MFALevel:
        """Update the MFA (Multi Factor Authentication) level for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#modify-guild-mfa-level

        Args:
            guild_id: ID of the guild to update.
            level: MFA level to set.

        Returns:
            Updated MFA level.
        """
        url = self.guilds_url / str(guild_id) / 'mfa'
        payload = {'level': level}
        resp = await self._http_client.post(url=url, payload=payload)
        return MFALevel(int(resp.raw_body))

    async def get_prune_count(
        self,
        guild_id: SnowflakeInputType,
        days: int | None = None,
        include_roles: Sequence[SnowflakeInputType] | None = None,
        reason: str | None = None,
    ) -> PruneResponse:
        """Get the number of members that would be removed from a guild if pruned.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-prune-count

        Args:
            guild_id: ID of the guild to get the prune count for.
            days: Number of days to count prune for. Should be between 1 and 30. Defaults to 7.
            include_roles: List of role IDs to include in the prune count.
            reason: Reason for the prune.

        Returns:
            Count of members that would be removed from the guild if pruned.
        """
        url_params = {}
        if days is not None:
            url_params['days'] = days
        if include_roles is not None:
            url_params['include_roles'] = ','.join(map(str, include_roles))

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        url = self.guilds_url / str(guild_id) / 'prune' % url_params
        resp = await self._http_client.get(url=url, headers=headers)
        return PruneResponse.model_validate(resp.body)

    async def begin_prune(
        self,
        *,
        guild_id: SnowflakeInputType,
        prune_data: PruneRequest,
        reason: str | None = None,
    ) -> PruneResponse:
        """Begin pruning a guild.

        For large guilds it's recommended to set the compute_prune_count option to false,
        forcing pruned to null. Fires multiple Guild Member Remove Gateway events.

        By default, prune will not remove users with roles. You can optionally
        include specific roles in your prune by providing the include_roles parameter.
        Any inactive user that has a subset of the provided role(s) will be
        included in the prune and users with additional roles will not.

        Reference:
        https://discord.com/developers/docs/resources/guild#begin-guild-prune

        Args:
            guild_id: ID of the guild to prune.
            prune_data: Data to prune the guild with.
            reason: Reason for the prune.

        Returns:
            Prune object.
        """
        payload = prune_data.model_dump(mode='json', exclude_unset=True)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        url = self.guilds_url / str(guild_id) / 'prune'
        resp = await self._http_client.post(url=url, payload=payload, headers=headers)
        return PruneResponse.model_validate(resp.body)

    async def get_voice_regions(self, guild_id: SnowflakeInputType) -> list[VoiceRegionResponse]:
        """Get the voice regions for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-voice-regions

        Args:
            guild_id: ID of the guild to get the voice regions for.

        Returns:
            Voice regions for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'regions'
        resp = await self._http_client.get(url=url)
        return list_model(VoiceRegionResponse).validate_python(resp.body)

    async def get_invites(self, guild_id: SnowflakeInputType) -> list[InviteResponse]:
        """Get the invites for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-invites

        Args:
            guild_id: ID of the guild to get the invites for.

        Returns:
            Invites for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'invites'
        resp = await self._http_client.get(url=url)
        return list_model(InviteResponse).validate_python(resp.body)

    async def get_channels(self, guild_id: SnowflakeInputType) -> list[ChannelResponse]:
        """Get the channels for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-channels

        Args:
            guild_id: ID of the guild to get the channels for.

        Returns:
            Channels for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'channels'
        resp = await self._http_client.get(url=url)
        return list_model(ChannelResponse).validate_python(resp.body)

    async def get_integrations(self, guild_id: SnowflakeInputType) -> list[IntegrationResponse]:
        """Get the integrations for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-integrations

        Args:
            guild_id: ID of the guild to get the integrations for.

        Returns:
            Integrations for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'integrations'
        resp = await self._http_client.get(url=url)
        return list_model(IntegrationResponse).validate_python(resp.body)

    async def delete_integration(
        self,
        guild_id: SnowflakeInputType,
        integration_id: SnowflakeInputType,
        reason: str | None = None,
    ) -> None:
        """Delete an integration.

        Reference:
        https://discord.com/developers/docs/resources/guild

        Args:
            guild_id: ID of the guild to delete the integration for.
            integration_id: ID of the integration to delete.
            reason: Reason for deleting the integration.
        """
        url = self.guilds_url / str(guild_id) / 'integrations' / str(integration_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        await self._http_client.delete(url=url, headers=headers)

    async def get_widget(
        self,
        guild_id: SnowflakeInputType,
    ) -> WidgetResponse:
        """Get the widget for a guild."""
        url = self.guilds_url / str(guild_id) / 'widget.json'
        resp = await self._http_client.get(url=url)
        return WidgetResponse.model_validate(resp.body)

    async def get_widget_settings(
        self,
        guild_id: SnowflakeInputType,
    ) -> WidgetSettingsResponse:
        """Get the widget settings for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-widget-settings

        Args:
            guild_id: ID of the guild to get the widget for.
        """
        url = self.guilds_url / str(guild_id) / 'widget'
        resp = await self._http_client.get(url=url)
        return WidgetSettingsResponse.model_validate(resp.body)

    async def update_widget(
        self,
        guild_id: SnowflakeInputType,
        widget_data: UpdateWidgetSettingsRequest,
        reason: str | None = None,
    ) -> WidgetSettingsResponse:
        """Update the widget for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#modify-guild-widget

        Args:
            guild_id: ID of the guild to update the widget for.
            widget_data: Data to update the widget with.
            reason: Reason for updating the widget.
        """
        url = self.guilds_url / str(guild_id) / 'widget'

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = widget_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(url=url, payload=payload, headers=headers)
        return WidgetSettingsResponse.model_validate(resp.body)

    async def get_widget_image(
        self,
        guild_id: SnowflakeInputType,
        style: WidgetStyleOptions | None = None,
    ) -> Base64Image:
        """Get the widget image for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-widget-image

        Args:
            guild_id: ID of the guild to get the widget image for.
            style: Style of the widget image.
        """
        url = self.guilds_url / str(guild_id) / 'widget.png'
        if style is not None:
            url %= {'style': style}

        resp = await self._http_client.get(url=url)
        return Base64Image.build(resp.raw_body)

    async def get_onboarding(
        self,
        guild_id: SnowflakeInputType,
    ) -> OnboardingResponse:
        """Get onboarding object for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-onboarding

        Args:
            guild_id: ID of the guild to get the welcome screen for.
        """
        url = self.guilds_url / str(guild_id) / 'onboarding'
        resp = await self._http_client.get(url=url)
        return OnboardingResponse.model_validate(resp.body)

    async def update_onboarding(
        self,
        guild_id: SnowflakeInputType,
        onboarding_data: UpdateOnboardingRequest,
        reason: str | None = None,
    ) -> OnboardingResponse:
        """Update the onboarding object for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#modify-guild-onboarding

        Args:
            guild_id: ID of the guild to update the onboarding for.
            onboarding_data: Onboarding data to update.
            reason: Reason for updating the onboarding.
        """
        url = self.guilds_url / str(guild_id) / 'onboarding'

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = onboarding_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.put(url=url, payload=payload, headers=headers)
        return OnboardingResponse.model_validate(resp.body)

    async def get_welcome_screen(self, guild_id: SnowflakeInputType) -> WelcomeScreenResponse:
        """Get the welcome screen for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-welcome-screen

        Args:
            guild_id: ID of the guild to get the welcome screen for.

        Returns:
            Welcome screen for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'welcome-screen'
        resp = await self._http_client.get(url=url)
        return WelcomeScreenResponse.model_validate(resp.body)

    async def update_welcome_screen(
        self,
        guild_id: SnowflakeInputType,
        welcome_screen_data: UpdateWelcomeScreenRequest,
        reason: str | None = None,
    ) -> WelcomeScreenResponse:
        """Update the welcome screen for a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#update-guild-welcome-screen

        Args:
            guild_id: ID of the guild to update the welcome screen for.
            welcome_screen_data: Welcome screen data to update.
            reason: Reason for updating the welcome screen.

        Returns:
            Updated welcome screen.
        """
        url = self.guilds_url / str(guild_id) / 'welcome-screen'

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = welcome_screen_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(url=url, payload=payload, headers=headers)
        return WelcomeScreenResponse.model_validate(resp.body)

    async def update_current_user_voice_state(
        self,
        guild_id: SnowflakeInputType,
        channel_id: SnowflakeInputType | None = None,
        suppress: bool | None = None,
        request_to_speak_timestamp: datetime.datetime | None = None,
    ) -> None:
        """Update the current user's voice state.

        Reference:
        https://discord.com/developers/docs/resources/guild#modify-current-user-voice-state

        Args:
            guild_id: ID of the guild to update the current user's voice state for.
            channel_id: ID of the channel to move the current user to.
            suppress: Whether the current user should be suppressed.
            request_to_speak_timestamp: Time at which the current user requested to speak.
        """
        url = self.guilds_url / str(guild_id) / 'voice-states' / CURRENT_USER

        payload = {}
        if channel_id is not None:
            payload['channel_id'] = str(channel_id)
        if suppress is not None:
            payload['suppress'] = suppress
        if request_to_speak_timestamp is not None:
            payload['request_to_speak_timestamp'] = request_to_speak_timestamp.isoformat()
        await self._http_client.patch(url=url, payload=payload)

    async def update_user_voice_state(
        self,
        guild_id: SnowflakeInputType,
        user_id: SnowflakeInputType,
        channel_id: SnowflakeInputType | None = None,
        suppress: bool | None = None,
    ) -> None:
        """Update a user's voice state.

        Reference:
        https://discord.com/developers/docs/resources/guild#modify-user-voice-state

        Args:
            guild_id: ID of the guild to update the user's voice state for.
            user_id: ID of the user to update the voice state for.
            channel_id: ID of the channel to move the user to.
            suppress: Whether the user should be suppressed.
        """
        url = self.guilds_url / str(guild_id) / 'voice-states' / str(user_id)

        payload = {}
        if channel_id is not None:
            payload['channel_id'] = str(channel_id)
        if suppress is not None:
            payload['suppress'] = suppress
        await self._http_client.patch(url=url, payload=payload)

    async def get_audit_log(
        self,
        guild_id: SnowflakeInputType,
        user_id: SnowflakeInputType | None = None,
        action_type: int | None = None,
        before: SnowflakeInputType | None = None,
        after: SnowflakeInputType | None = None,
        limit: int | None = None,
    ) -> AuditLogResponse:
        """Get the audit log for a guild.

        Reference:
        https://discord.com/developers/docs/resources/audit-log#get-guild-audit-log

        Args:
            guild_id: ID of the guild to get the audit log for.
            user_id: ID of the user to filter the log by.
            action_type: Type of action to filter the log by.
            before: ID of the entry to get entries before.
            after: ID of the entry to get entries after.
            limit: Number of entries to get.
        """
        query_params = {}
        if user_id is not None:
            query_params['user_id'] = user_id
        if action_type is not None:
            query_params['action_type'] = action_type
        if before is not None:
            query_params['before'] = before
        if after is not None:
            query_params['after'] = after
        if limit is not None:
            query_params['limit'] = limit

        url = self.guilds_url / str(guild_id) / 'audit-logs' % query_params

        resp = await self._http_client.get(url=url)
        return AuditLogResponse.model_validate(resp.body)

    async def get_list_auto_moderation_rules(
        self,
        guild_id: SnowflakeInputType,
    ) -> list[AutoModerationRule]:
        """Get a list of all rules currently configured for the guild.

        Args:
            guild_id: ID of the guild to get the rules for.

        Reference:
        https://discord.com/developers/docs/resources/auto-moderation#list-auto-moderation-rules-for-guild
        """
        url = self.guilds_url / str(guild_id) / 'auto-moderation' / 'rules'
        resp = await self._http_client.get(url=url)
        return list_model(AutoModerationRule).validate_python(resp.body)

    async def get_auto_moderation_rule(
        self,
        guild_id: SnowflakeInputType,
        rule_id: SnowflakeInputType,
    ) -> AutoModerationRule:
        """Get a single rule.

        Args:
            guild_id: ID of the guild to get the rule for.
            rule_id: ID of the rule to get.

        Reference:
        https://discord.com/developers/docs/resources/auto-moderation#get-auto-moderation-rule
        """
        url = self.guilds_url / str(guild_id) / 'auto-moderation' / 'rules' / str(rule_id)
        resp = await self._http_client.get(url=url)
        return AutoModerationRule.model_validate(resp.body)

    async def create_auto_moderation_rule(
        self,
        guild_id: SnowflakeInputType,
        rule: CreateAutoModerationRuleRequest,
    ) -> AutoModerationRule:
        """Create a new rule. Returns an auto moderation rule on success.

        Reference:
        https://discord.com/developers/docs/resources/auto-moderation#create-auto-moderation-rule
        """
        url = self.guilds_url / str(guild_id) / 'auto-moderation' / 'rules'
        payload = rule.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url=url, payload=payload)
        return AutoModerationRule.model_validate(resp.body)

    async def update_auto_moderation_rule(
        self,
        guild_id: SnowflakeInputType,
        rule_id: SnowflakeInputType,
        rule: UpdateAutoModerationRuleRequest,
    ) -> AutoModerationRule:
        """Update an existing rule. Returns an auto moderation rule on success.

        Reference:
        https://discord.com/developers/docs/resources/auto-moderation#modify-auto-moderation-rule
        """
        url = self.guilds_url / str(guild_id) / 'auto-moderation' / 'rules' / str(rule_id)
        payload = rule.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(url=url, payload=payload)
        return AutoModerationRule.model_validate(resp.body)

    async def delete_auto_moderation_rule(
        self,
        guild_id: SnowflakeInputType,
        rule_id: SnowflakeInputType,
    ) -> None:
        """Delete a rule.

        Reference:
        https://discord.com/developers/docs/resources/auto-moderation#delete-auto-moderation-rule
        """
        url = self.guilds_url / str(guild_id) / 'auto-moderation' / 'rules' / str(rule_id)
        await self._http_client.delete(url=url)

    async def get_vanity_url(
        self,
        guild_id: SnowflakeInputType,
    ) -> VanityUrlInviteResponse:
        """Returns a partial invite for guilds with that feature.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-vanity-url

        Args:
            guild_id: ID of the guild to get the vanity url for.
        """
        url = self.guilds_url / str(guild_id) / 'vanity-url'
        resp = await self._http_client.get(url=url)
        return VanityUrlInviteResponse.model_validate(resp.body)
