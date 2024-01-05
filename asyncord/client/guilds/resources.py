"""This module contains the guilds resource endpoints.

Reference: https://discord.com/developers/docs/resources/guild
"""

from __future__ import annotations

import datetime

from asyncord.client.bans.resources import BanResource
from asyncord.client.channels.models.output import ChannelOutput
from asyncord.client.guilds.models import (
    CreateGuildInput,
    GuildOutput,
    GuildPreviewOutput,
    IntegrationOutput,
    InviteOutput,
    MFALevel,
    PruneOutput,
    UpdateWelcomeScreenInput,
    VoiceRegionOutput,
    WelcomeScreenOutput,
)
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.members.resources import MemberResource
from asyncord.client.resources import ClientSubresource
from asyncord.client.roles.resources import RoleResource
from asyncord.client.scheduled_events.resources import ScheduledEventsResource
from asyncord.snowflake import SnowflakeInput
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL


class GuildResource(ClientSubresource):
    """Representaion of the guilds resource.

    Attributes:
        guilds_url: Guilds resource URL.
    """

    guilds_url = REST_API_URL / 'guilds'

    def members(self, guild_id: SnowflakeInput) -> MemberResource:
        """Get the member subresource for a guild.

        Args:
            guild_id: ID of guild to get the member subresource for.

        Returns:
            Member subresource for the guild.
        """
        return MemberResource(self, guild_id)

    def ban_managment(self, guild_id: SnowflakeInput) -> BanResource:
        """Get the ban subresource for a guild.

        Args:
            guild_id: ID of the guild to get the ban subresource for.

        Returns:
            Ban subresource for the guild.
        """
        return BanResource(self, guild_id)

    def roles(self, guild_id: SnowflakeInput) -> RoleResource:
        """Get the role subresource for a guild.

        Args:
            guild_id: ID of the guild to get the role subresource for.

        Returns:
            Role subresource for the guild.
        """
        return RoleResource(self, guild_id)

    def events(self, guild_id: SnowflakeInput) -> ScheduledEventsResource:
        """Get the events subresource for a guild.

        Args:
            guild_id: ID of the guild to get the events subresource for.

        Returns:
            Events subresource for the guild.
        """
        return ScheduledEventsResource(self, guild_id)

    async def get(self, guild_id: SnowflakeInput, with_counts: bool = False) -> GuildOutput:
        """Get a guild.

        Reference: https://discord.com/developers/docs/resources/guild#et-guild

        Args:
            guild_id: ID of the guild to get.
            with_counts: Whether to include approximate members.

        Returns:
            Guild with the specified ID.
        """
        url = self.guilds_url / str(guild_id) % {'with_counts': str(with_counts)}
        resp = await self._http_client.get(url)
        return GuildOutput.model_validate(resp.body)

    async def get_preview(self, guild_id: SnowflakeInput) -> GuildPreviewOutput:
        """Get a guild preview.

        Preview guilds are a special type of guilds object that contain only
        the most vital information about a guild.

        Args:
            guild_id: ID of the guild to get the preview for.

        Returns:
            Preview of the guild with the specified ID.
        """
        url = self.guilds_url / str(guild_id) / 'preview'
        resp = await self._http_client.get(url)
        return GuildPreviewOutput.model_validate(resp.body)

    async def create(self, guild_data: CreateGuildInput) -> GuildOutput:
        """Create a new guild.

        This endpoint can be used only by bots in less than 10 guilds.

        Reference: https://discord.com/developers/docs/resources/guild#create-guild

        Args:
            guild_data(CreateGuildData): The data for the guild to create.

        Returns:
            The created guild.
        """
        payload = guild_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(self.guilds_url, payload)
        return GuildOutput.model_validate(resp.body)

    async def delete(self, guild_id: SnowflakeInput) -> None:
        """Delete a guild.

        Args:
            guild_id: ID of the guild to delete.
        """
        url = self.guilds_url / str(guild_id)
        await self._http_client.delete(url)

    async def update_mfa(self, guild_id: SnowflakeInput, level: MFALevel) -> MFALevel:
        """Update the MFA (Multi Factor Authentication) level for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#modify-guild-mfa-level

        Args:
            guild_id: ID of the guild to update.
            level: MFA level to set.

        Returns:
            Updated MFA level.
        """
        url = self.guilds_url / str(guild_id) / 'mfa'
        payload = {'level': level}
        resp = await self._http_client.patch(url, payload)
        return MFALevel(int(resp.body))

    async def get_prune_count(
        self,
        guild_id: SnowflakeInput,
        days: int | None = None,
        include_roles: list[SnowflakeInput] | None = None,
        reason: str | None = None,
    ) -> PruneOutput:
        """Get the number of members that would be removed from a guild if pruned.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-prune-count

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

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        url = self.guilds_url / str(guild_id) / 'prune' % url_params
        resp = await self._http_client.get(url, headers)
        return PruneOutput.model_validate(resp.body)

    # TODO: #15 Replace args with a dataclass
    async def begin_prune(  # noqa: PLR0913
        self,
        guild_id: SnowflakeInput,
        days: int | None = None,
        compute_prune_count: bool | None = None,
        include_roles: list[SnowflakeInput] | None = None,
        reason: str | None = None,
    ) -> PruneOutput:
        """Begin pruning a guild.

        For large guilds it's recommended to set the compute_prune_count option to false,
        forcing pruned to null. Fires multiple Guild Member Remove Gateway events.

        By default, prune will not remove users with roles. You can optionally
        include specific roles in your prune by providing the include_roles parameter.
        Any inactive user that has a subset of the provided role(s) will be
        included in the prune and users with additional roles will not.

        Reference: https://discord.com/developers/docs/resources/guild#begin-guild-prune

        Args:
            guild_id: ID of the guild to prune.
            days: Number of days to count prune for. Should be between 1 and 30. Defaults to 7.
            compute_prune_count: Whether to compute the prune count. Defaults to True.
            include_roles: List of role IDs to include in the prune count.
            reason: Reason for the prune.

        Returns:
            Prune object.
        """
        payload = {}
        if days is not None:
            payload['days'] = days
        if compute_prune_count is not None:
            payload['compute_prune_count'] = compute_prune_count
        if include_roles is not None:
            payload['include_roles'] = ','.join(map(str, include_roles))

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        url = self.guilds_url / str(guild_id) / 'prune'
        resp = await self._http_client.post(url, payload, headers=headers)
        return PruneOutput.model_validate(resp.body)

    async def get_voice_regions(self, guild_id: SnowflakeInput) -> list[VoiceRegionOutput]:
        """Get the voice regions for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-voice-regions

        Args:
            guild_id: ID of the guild to get the voice regions for.

        Returns:
            Voice regions for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'regions'
        resp = await self._http_client.get(url)
        return list_model(VoiceRegionOutput).validate_python(resp.body)

    async def get_invites(self, guild_id: SnowflakeInput) -> list[InviteOutput]:
        """Get the invites for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-invites

        Args:
            guild_id: ID of the guild to get the invites for.

        Returns:
            Invites for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'invites'
        resp = await self._http_client.get(url)
        return list_model(InviteOutput).validate_python(resp.body)

    async def get_channels(self, guild_id: SnowflakeInput) -> list[ChannelOutput]:
        """Get the channels for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-channels

        Args:
            guild_id: ID of the guild to get the channels for.

        Returns:
            Channels for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'channels'
        resp = await self._http_client.get(url)
        return list_model(ChannelOutput).validate_python(resp.body)

    async def get_integrations(self, guild_id: SnowflakeInput) -> list[IntegrationOutput]:
        """Get the integrations for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-integrations

        Args:
            guild_id: ID of the guild to get the integrations for.

        Returns:
            Integrations for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'integrations'
        resp = await self._http_client.get(url)
        return list_model(IntegrationOutput).validate_python(resp.body)

    async def delete_integration(
        self,
        guild_id: SnowflakeInput,
        integration_id: SnowflakeInput,
        reason: str | None = None,
    ) -> None:
        """Delete an integration.

        Reference: https://discord.com/developers/docs/resources/guild

        Args:
            guild_id: ID of the guild to delete the integration for.
            integration_id: ID of the integration to delete.
            reason: Reason for deleting the integration.
        """
        url = self.guilds_url / str(guild_id) / 'integrations' / str(integration_id)

        if reason is None:
            headers = {}
        else:
            headers = {AUDIT_LOG_REASON: reason}

        await self._http_client.delete(url, headers=headers)

    async def get_welcome_screen(self, guild_id: SnowflakeInput) -> WelcomeScreenOutput:
        """Get the welcome screen for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-welcome-screen

        Args:
            guild_id: ID of the guild to get the welcome screen for.

        Returns:
            Welcome screen for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'welcome-screen'
        resp = await self._http_client.get(url)
        return WelcomeScreenOutput.model_validate(resp.body)

    async def update_welcome_screen(
        self,
        guild_id: SnowflakeInput,
        welcome_screen_data: UpdateWelcomeScreenInput,
        reason: str | None = None,
    ) -> WelcomeScreenOutput:
        """Update the welcome screen for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#update-guild-welcome-screen

        Args:
            guild_id: ID of the guild to update the welcome screen for.
            welcome_screen_data: Welcome screen data to update.
            reason: Reason for updating the welcome screen.

        Returns:
            Updated welcome screen.
        """
        url = self.guilds_url / str(guild_id) / 'welcome-screen'

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload = welcome_screen_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(url, payload, headers=headers)
        return WelcomeScreenOutput.model_validate(resp.body)

    async def update_current_user_voice_state(
        self,
        guild_id: SnowflakeInput,
        channel_id: SnowflakeInput | None = None,
        suppress: bool | None = None,
        request_to_speak_timestamp: datetime.datetime | None = None,
    ) -> None:
        """Update the current user's voice state.

        Reference: https://discord.com/developers/docs/resources/guild#modify-current-user-voice-state

        Args:
            guild_id: ID of the guild to update the current user's voice state for.
            channel_id: ID of the channel to move the current user to.
            suppress: Whether the current user should be suppressed.
            request_to_speak_timestamp: Time at which the current user requested to speak.
        """
        url = self.guilds_url / str(guild_id) / 'voice-states' / '@me'

        payload = {}
        if channel_id is not None:
            payload['channel_id'] = str(channel_id)
        if suppress is not None:
            payload['suppress'] = suppress
        if request_to_speak_timestamp is not None:
            payload['request_to_speak_timestamp'] = request_to_speak_timestamp.isoformat()
        await self._http_client.patch(url, payload)

    async def update_user_voice_state(
        self,
        guild_id: SnowflakeInput,
        user_id: SnowflakeInput,
        channel_id: SnowflakeInput | None = None,
        suppress: bool | None = None,
    ) -> None:
        """Update a user's voice state.

        Reference: https://discord.com/developers/docs/resources/guild#modify-user-voice-state

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
        await self._http_client.patch(url, payload)
