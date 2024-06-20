"""This module contains the ScheduledEventsResource class -- a resource to perform actions on guild events.

Reference:
https://discord.com/developers/docs/resources/guild-scheduled-event
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.http.headers import AUDIT_LOG_REASON
from asyncord.client.resources import APIResource
from asyncord.client.scheduled_events.models.responses import ScheduledEventResponse, ScheduledEventUserResponse
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.client.scheduled_events.models.requests import (
        CreateScheduledEventRequest,
        UpdateScheduledEventRequest,
    )
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('ScheduledEventsResource',)


class ScheduledEventsResource(APIResource):
    """Resource to perform actions on guild scheduled events.

    Attributes:
        guilds_url: URL for the guilds resource.
    """

    guilds_url = REST_API_URL / 'guilds'

    def __init__(self, http_client: HttpClient, guild_id: SnowflakeInputType):
        """Create a new scheduled events resource."""
        super().__init__(http_client)
        self.guild_id = guild_id
        self.events_url = self.guilds_url / str(self.guild_id) / 'scheduled-events'

    async def get(self, event_id: SnowflakeInputType, with_user_count: bool = False) -> ScheduledEventResponse:
        """Get a scheduled event of a guild.

        Args:
            event_id: ID of the event to get.
            with_user_count: Whether to include the number of users who have signed up for this event.

        Returns:
            GuildScheduleEvent object for the ID provided.
        """
        url = self.events_url / str(event_id) % {'with_user_count': str(with_user_count)}
        resp = await self._http_client.get(url=url)
        return ScheduledEventResponse.model_validate(resp.body)

    async def get_list(self, with_user_count: bool = False) -> list[ScheduledEventResponse]:
        """Get a list of scheduled events of a guild.

        Args:
            with_user_count: Whether to include the number of users who have signed up for this event.

        Returns:
            List of GuildScheduleEvent objects.
        """
        url = self.events_url % {'with_user_count': str(with_user_count)}
        resp = await self._http_client.get(url=url)
        return list_model(ScheduledEventResponse).validate_python(resp.body)

    async def create(
        self,
        event_data: CreateScheduledEventRequest,
        reason: str | None = None,
    ) -> ScheduledEventResponse:
        """Create a scheduled event.

        Args:
            event_data: Event to create.
            reason: Reason for audit logs.

        Returns:
            Created event.
        """
        if reason:
            headers = {AUDIT_LOG_REASON: reason}
        else:
            headers = {}

        paylod = event_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.post(url=self.events_url, payload=paylod, headers=headers)
        return ScheduledEventResponse.model_validate(resp.body)

    async def update(
        self,
        event_id: SnowflakeInputType,
        event_data: UpdateScheduledEventRequest,
    ) -> ScheduledEventResponse:
        """Update a scheduled event.

        Args:
            event_id: ID of the event to update.
            event_data: Event data to update.

        Returns:
            Updated event.
        """
        url = self.events_url / str(event_id)
        payload = event_data.model_dump(mode='json', exclude_unset=True)
        resp = await self._http_client.patch(url=url, payload=payload)
        return ScheduledEventResponse.model_validate(resp.body)

    async def delete(self, event_id: SnowflakeInputType) -> None:
        """Delete a scheduled event.

        Args:
            event_id: ID of the event to delete.
        """
        url = self.events_url / str(event_id)
        await self._http_client.delete(url=url)

    async def get_event_users(self, event_id: SnowflakeInputType) -> list[ScheduledEventUserResponse]:
        """Get a list of users who have signed up for a scheduled event.

        Args:
            event_id: ID of the event to get users for.

        Returns:
            List of users who have signed up for the event.
        """
        url = self.events_url / str(event_id) / 'users'
        resp = await self._http_client.get(url=url)
        return list_model(ScheduledEventUserResponse).validate_python(resp.body)
