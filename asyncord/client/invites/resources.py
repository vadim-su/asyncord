"""Intive Resource Endpoints.

Reference:
https://discord.com/developers/docs/resources/invite#invite-resource
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.guilds.models.responses import InviteResponse
from asyncord.client.resources import APIResource
from asyncord.snowflake import SnowflakeInputType
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('InvitesResource',)


class InvitesResource(APIResource):
    """Invite Resource Endpoints.

    These endpoints are for managing invites.

    Reference:
    https://discord.com/developers/docs/resources/invite#invite-resource
    """

    invites_url = REST_API_URL / 'invites'

    async def get_invite(
        self,
        invite_code: str,
        with_counts: bool | None = None,
        with_expiration: bool | None = False,
        guild_scheduled_event_id: SnowflakeInputType | None = None,
    ) -> InviteResponse:
        """Get an invite by its code.

        Reference:
        https://discord.com/developers/docs/resources/invite#get-invite

        Args:
            invite_code (str): The invite code.
            with_counts (bool, optional):
                Whether the invite should contain approximate member counts.
            with_expiration (bool, optional):
                Whether the invite should contain approximate member counts.
            guild_scheduled_event_id (SnowflakeInputType, optional):
                Guild scheduled event to include with the invite.
        """
        query_param = {}

        if with_counts is not None:
            query_param['with_counts'] = str(with_counts)
        if with_expiration is not None:
            query_param['with_expiration'] = str(with_expiration)
        if guild_scheduled_event_id:
            query_param['guild_scheduled_event_id'] = str(guild_scheduled_event_id)

        url = self.invites_url / str(invite_code) % query_param

        resp = await self._http_client.get(url=url)
        return InviteResponse.model_validate(resp.body)

    async def delete_invite(
        self,
        invite_code: str,
        reason: str | None = None,
    ) -> InviteResponse:
        """Delete an invite by its code.

        Reference:
        https://discord.com/developers/docs/resources/invite#delete-invite
        """
        if reason:
            headers = {'X-Audit-Log-Reason': reason}
        else:
            headers = {}

        url = self.invites_url / str(invite_code)

        resp = await self._http_client.delete(url=url, headers=headers)
        return InviteResponse.model_validate(resp.body)
