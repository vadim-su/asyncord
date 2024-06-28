"""This module contains the ban resource classes."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from asyncord.client.bans.models.responses import BanResponse, BulkBanResponse
from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.resources import APIResource
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('BanResource',)


class BanResource(APIResource):
    """Base class for ban resources.

    Attributes:
        guilds_url: Base guilds url.
    """

    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, http_client: HttpClient, guild_id: SnowflakeInputType):
        """Initialize the ban resource."""
        super().__init__(http_client)
        self.guild_id = guild_id
        self.bans_url = self.guilds_url / str(self.guild_id) / 'bans'

    async def get(self, user_id: SnowflakeInputType) -> BanResponse:
        """Get a ban object for a user.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-ban

        Args:
            user_id: ID of the user to get the ban object for.
        """
        url = self.bans_url / str(user_id)
        resp = await self._http_client.get(url=url)
        return BanResponse.model_validate(resp.body)

    async def get_list(
        self,
        limit: int | None = None,
        before: SnowflakeInputType | None = None,
        after: SnowflakeInputType | None = None,
    ) -> list[BanResponse]:
        """List bans of a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#get-guild-bans

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
        resp = await self._http_client.get(url=url)
        return list_model(BanResponse).validate_python(resp.body)

    async def ban(
        self,
        user_id: SnowflakeInputType,
        delete_message_seconds: int | None = None,
        reason: str | None = None,
    ) -> None:
        """Ban a user from a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#create-guild-ban

        Args:
            user_id: ID of a user to ban.
            delete_message_seconds: number of seconds to delete messages for.
                between 0 and 604800 (7 days). Defaults to 0.
            reason: Reason for banning the user. Defaults to None.
        """
        url = self.bans_url / str(user_id)

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        if delete_message_seconds is not None:
            payload = {'delete_message_seconds': delete_message_seconds}
        else:
            payload = None

        await self._http_client.put(url=url, payload=payload, headers=headers)

    async def unban(self, user_id: SnowflakeInputType, reason: str | None = None) -> None:
        """Unban a user from a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#remove-guild-ban

        Args:
            user_id: ID of the user to unban.
            reason: Reason for unbanning the user. Defaults to None.
        """
        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}
        url = self.bans_url / str(user_id)
        await self._http_client.delete(url=url, headers=headers)

    async def bulk_ban(
        self,
        user_ids: Sequence[SnowflakeInputType],
        delete_message_seconds: int | None = None,
        reason: str | None = None,
    ) -> BulkBanResponse:
        """Ban up to 200 users from a guild.

        Reference:
        https://discord.com/developers/docs/resources/guild#create-guild-ban

        Args:
            user_ids: List of user IDs to ban.
            delete_message_seconds: number of seconds to delete messages for.
                between 0 and 604800 (7 days). Defaults to 0.
            reason: Reason for banning the users. Defaults to None.
        """
        url = self.guilds_url / str(self.guild_id) / 'bulk-ban'

        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        payload: dict[str, Any] = {
            'user_ids': user_ids,
        }

        if delete_message_seconds is not None:
            payload['delete_message_seconds'] = delete_message_seconds

        resp = await self._http_client.post(
            url=url,
            payload=payload,
            headers=headers,
        )
        return BulkBanResponse.model_validate(resp.body)
