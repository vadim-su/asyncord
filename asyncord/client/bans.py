"""This module contains the ban resource classes."""

from __future__ import annotations

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.models.bans import Ban
from asyncord.client.resources import ClientResource, ClientSubresources
from asyncord.typedefs import LikeSnowflake, list_model
from asyncord.urls import REST_API_URL


class BanResource(ClientSubresources):
    """Base class for ban resources.

    Attributes:
        guilds_url (URL): Base guilds url.
    """

    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, parent: ClientResource, guild_id: LikeSnowflake):
        """Initialize the ban resource."""
        super().__init__(parent)
        self.guild_id = guild_id
        self.bans_url = self.guilds_url / str(self.guild_id) / 'bans'

    async def get(self, user_id: LikeSnowflake) -> Ban:
        """Get a ban object for a user."""
        url = self.bans_url / str(user_id)
        resp = await self._http.get(url)
        return Ban.model_validate(resp.body)

    async def get_list(
        self,
        limit: int | None = None,
        before: LikeSnowflake | None = None,
        after: LikeSnowflake | None = None,
    ) -> list[Ban]:
        """List bans of a guild.

        Args:
            limit (int | None): Number of bans to return. Defaults to None.
            before (LikeSnowflake | None): ID of the ban to get bans before. Defaults to None.
            after (LikeSnowflake | None): ID of the ban to get bans after. Defaults to None.

        Returns:
            list[Ban]: list of user bans.
        """
        url_params = {}
        if limit is not None:
            url_params['limit'] = limit
        if before is not None:
            url_params['before'] = before
        if after is not None:
            url_params['after'] = after

        url = self.bans_url % url_params
        resp = await self._http.get(url)
        return list_model(Ban).validate_python(resp.body)

    async def ban(
        self,
        user_id: LikeSnowflake,
        delete_message_days: int | None = None,
        reason: str | None = None,
    ) -> None:
        """Ban a user from a guild.

        Args:
            user_id (LikeSnowflake): The ID of the user to ban.
            delete_message_days (int | None): The number of days to delete messages for.
                Should be between 0 and 7. Defaults to 0.
            reason (str | None): The reason for banning the user. Defaults to None.
        """
        url = self.bans_url / str(user_id)

        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        if delete_message_days is not None:
            payload = {'delete_message_days': delete_message_days}
        else:
            payload = None

        await self._http.put(url, payload, headers=headers)

    async def unban(self, user_id: LikeSnowflake, reason: str | None = None) -> None:
        """Unban a user from a guild.

        Args:
            user_id (LikeSnowflake): The ID of the user to unban.
            reason (str | None): The reason for unbanning the user. Defaults to None.
        """
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        url = self.bans_url / str(user_id)
        await self._http.delete(url, headers=headers)
