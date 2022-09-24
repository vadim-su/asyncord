from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.urls import REST_API_URL
from asyncord.client.bans import BanResource
from asyncord.client.roles import RoleResource
from asyncord.client.headers import AUDIT_LOG_REASON
from asyncord.client.members import MemberResource
from asyncord.client.resources import ClientSubresources
from asyncord.client.models.guilds import (
    Guild,
    Prune,
    Invite,
    MFALevel,
    VoiceRegion,
    GuildPreview,
    CreateGuildData,
)

if TYPE_CHECKING:
    from asyncord.typedefs import LikeSnowflake


class GuildResource(ClientSubresources):
    guilds_url = REST_API_URL / 'guilds'

    def members(self, guild_id: LikeSnowflake) -> MemberResource:
        """Get the member subresource for a guild.

        Arguments:
            guild_id (LikeSnowflake): The ID of the guild to get the member subresource for.

        Returns:
            MemberResource: The member subresource for the guild.
        """
        return MemberResource(self, guild_id)

    def ban_managment(self, guild_id: LikeSnowflake) -> BanResource:
        """Get the ban subresource for a guild.

        Arguments:
            guild_id (LikeSnowflake): The ID of the guild to get the ban subresource for.

        Returns:
            BanResource: The ban subresource for the guild.
        """
        return BanResource(self, guild_id)

    def roles(self, guild_id: LikeSnowflake) -> RoleResource:
        """Get the role subresource for a guild.

        Arguments:
            guild_id (LikeSnowflake): The ID of the guild to get the role subresource for.

        Returns:
            RoleResource: The role subresource for the guild.
        """
        return RoleResource(self, guild_id)

    async def get(self, guild_id: LikeSnowflake, with_counts: bool | None = None) -> Guild:
        """Get a guild.

        Reference: https://discord.com/developers/docs/resources/guild#et-guild

        Arguments:
            guild_id(LikeSnowflake): The ID of the guild to get.
            with_counts(bool | None): Whether to include approximate members.

        Returns:
            Guild: The guild with the specified ID.
        """
        # FIXME: with_counts is not implemented
        url = self.guilds_url / str(guild_id)
        resp = await self._http.get(url)
        return Guild(**resp.body)

    async def get_preview(self, guild_id: LikeSnowflake) -> GuildPreview:
        url = self.guilds_url / str(guild_id) / 'preview'
        resp = await self._http.get(url)
        return GuildPreview(**resp.body)

    async def create(self, guild_data: CreateGuildData) -> Guild:
        """Create a new guild.

        This endpoint can be used only by bots in less than 10 guilds.

        Reference: https://discord.com/developers/docs/resources/guild#create-guild

        Arguments:
            guild_data(CreateGuildData): The data for the guild to create.

        Returns:
            Guild: The created guild.
        """
        payload = guild_data.dict(exclude_unset=True)
        resp = await self._http.post(self.guilds_url, payload)
        return Guild(**resp.body)

    async def delete(self, guild_id: LikeSnowflake) -> None:
        """Delete a guild.

        Arguments:
            guild_id(LikeSnowflake): The ID of the guild to delete.
        """
        url = self.guilds_url / str(guild_id)
        await self._http.delete(url)

    async def update_mfa(self, guild_id: LikeSnowflake, level: MFALevel) -> MFALevel:
        """Update the MFA level for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#modify-guild-mfa

        Arguments:
            guild_id(LikeSnowflake): The ID of the guild to update.
            level(MFALevel): The MFA level to set.

        Returns:
            MFALevel: The updated MFA level.
        """
        url = self.guilds_url / str(guild_id) / 'mfa'
        payload = {'level': level}
        resp = await self._http.patch(url, payload)
        return MFALevel(int(resp.body))

    async def get_prune_count(
        self,
        guild_id: LikeSnowflake,
        days: int | None = None,
        include_roles: list[LikeSnowflake] | None = None,
        reason: str | None = None,
    ) -> Prune:
        """Get the number of members that would be removed from a guild if pruned.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-prune-count

        Arguments:
            guild_id(LikeSnowflake): The ID of the guild to get the prune count for.
            days(int | None): The number of days to count prune for. Should be between 1 and 30.
                Defaults to 7 if not specified.
            include_roles(list[LikeSnowflake] | None): A list of role IDs to include in
                the prune count.
            reason(str | None): The reason for the prune.

        Returns:
            int: The number of members that would be removed from the guild.
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
        resp = await self._http.get(url, headers)
        return Prune(**resp.body)

    async def begin_guild_prune(
        self,
        guild_id: LikeSnowflake,
        days: int | None = None,
        compute_prune_count: bool | None = None,
        include_roles: list[LikeSnowflake] | None = None,
        reason: str | None = None,
    ) -> Prune:
        """Begin pruning a guild.

        For large guilds it's recommended to set the compute_prune_count option to false,
        forcing pruned to null. Fires multiple Guild Member Remove Gateway events.

        By default, prune will not remove users with roles. You can optionally
        include specific roles in your prune by providing the include_roles parameter.
        Any inactive user that has a subset of the provided role(s) will be
        included in the prune and users with additional roles will not.

        Reference: https://discord.com/developers/docs/resources/guild#begin-guild-prune

        Arguments:
            guild_id(LikeSnowflake): The ID of the guild to prune.
            days(int | None): The number of days to count prune for. Should be between 1 and 30.
                Defaults to 7 if not specified.
            compute_prune_count(bool | None): Whether to compute the prune count.
                Defaults to True if not specified.
            include_roles(list[LikeSnowflake] | None): A list of role IDs to include in the prune count.
            reason(str | None): The reason for the prune.
        """
        url_params = {}
        if days is not None:
            url_params['days'] = days
        if compute_prune_count is not None:
            url_params['compute_prune_count'] = compute_prune_count
        if include_roles is not None:
            url_params['include_roles'] = ','.join(map(str, include_roles))

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        url = self.guilds_url / str(guild_id) / 'prune' % url_params
        resp = await self._http.post(url, headers)
        return Prune(**resp.body)

    async def get_voice_regions(self, guild_id: LikeSnowflake) -> list[VoiceRegion]:
        """Get the voice regions for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-voice-regions

        Arguments:
            guild_id(LikeSnowflake): The ID of the guild to get the voice regions for.

        Returns:
            list[VoiceRegion]: The voice regions for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'regions'
        resp = await self._http.get(url)
        return [VoiceRegion(**voice_region) for voice_region in resp.body]

    async def get_invites(self, guild_id: LikeSnowflake) -> list[Invite]:
        """Get the invites for a guild.

        Reference: https://discord.com/developers/docs/resources/guild#get-guild-invites

        Arguments:
            guild_id(LikeSnowflake): The ID of the guild to get the invites for.

        Returns:
            list[Invite]: The invites for the guild.
        """
        url = self.guilds_url / str(guild_id) / 'invites'
        resp = await self._http.get(url)
        return [Invite(**invite) for invite in resp.body]
