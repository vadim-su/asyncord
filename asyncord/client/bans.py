from __future__ import annotations

from asyncord.urls import REST_API_URL
from asyncord.typedefs import LikeSnowflake
from asyncord.client.resources import ClientResource, ClientSubresources
from asyncord.client.models.bans import Ban
from asyncord.client.http.headers import AUDIT_LOG_REASON


class BanResource(ClientSubresources):
    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, parent: ClientResource, guild_id: LikeSnowflake):
        super().__init__(parent)
        self.guild_id = guild_id
        self.bans_url = self.guilds_url / str(self.guild_id) / 'bans'

    async def get(self, user_id: LikeSnowflake) -> Ban:
        url = self.bans_url / str(user_id)
        resp = await self._http.get(url)
        return Ban(**resp.body)

    async def get_list(
        self,
        limit: int | None = None,
        before: LikeSnowflake | None = None,
        after: LikeSnowflake | None = None,
    ) -> list[Ban]:
        """List bans of a guild."""
        url_params = {}
        if limit is not None:
            url_params['limit'] = limit
        if before is not None:
            url_params['before'] = before
        if after is not None:
            url_params['after'] = after

        url = self.bans_url % url_params
        resp = await self._http.get(url)
        return [Ban(**ban) for ban in resp.body]

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

        await self._http.put(url, payload, headers)

    async def unban(self, user_id: LikeSnowflake, reason: str | None = None,) -> None:
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
