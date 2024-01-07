"""This module contains the ban resource classes."""

from __future__ import annotations

from asyncord.client.bans.models.responses import BanResponse
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.resources import ClientResource, ClientSubresource
from asyncord.snowflake import SnowflakeInputType
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL


class BanResource(ClientSubresource):
    """Base class for ban resources.

    Attributes:
        guilds_url: Base guilds url.
    """

    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, parent: ClientResource, guild_id: SnowflakeInputType):
        """Initialize the ban resource."""
        super().__init__(parent)
        self.guild_id = guild_id
        self.bans_url = self.guilds_url / str(self.guild_id) / 'bans'

    async def get(self, user_id: SnowflakeInputType) -> BanResponse:
        """Get a ban object for a user."""
        url = self.bans_url / str(user_id)
        resp = await self._http_client.get(url)
        return BanResponse.model_validate(resp.body)

    async def get_list(
        self,
        limit: int | None = None,
        before: SnowflakeInputType | None = None,
        after: SnowflakeInputType | None = None,
    ) -> list[BanResponse]:
        """List bans of a guild.

        Args:
            limit: Number of bans to return. Defaults to None.
            before: ID of the ban to get bans before. Defaults to None.
            after: ID of the ban to get bans after. Defaults to None.

        Returns:
            List of user bans.
        """
        url_params = {}
        if limit is not None:
            url_params['limit'] = limit
        if before is not None:
            url_params['before'] = before
        if after is not None:
            url_params['after'] = after

        url = self.bans_url % url_params
        resp = await self._http_client.get(url)
        return list_model(BanResponse).validate_python(resp.body)

    async def ban(
        self,
        user_id: SnowflakeInputType,
        delete_message_days: int | None = None,
        reason: str | None = None,
    ) -> None:
        """Ban a user from a guild.

        Args:
            user_id: ID of a user to ban.
            delete_message_days: Number of days to delete messages for.
                Should be between 0 and 7. Defaults to 0.
            reason: Reason for banning the user. Defaults to None.
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

        await self._http_client.put(url, payload, headers=headers)

    async def unban(self, user_id: SnowflakeInputType, reason: str | None = None) -> None:
        """Unban a user from a guild.

        Args:
            user_id: ID of the user to unban.
            reason: Reason for unbanning the user. Defaults to None.
        """
        if reason is not None:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        url = self.bans_url / str(user_id)
        await self._http_client.delete(url, headers=headers)
