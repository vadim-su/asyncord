"""This module contains models related to scheduled events in a guild."""

from asyncord.client.scheduled_events.models.responses import ScheduledEventResponse
from asyncord.gateway.events.base import GatewayEvent
from asyncord.snowflake import Snowflake

__all__ = (
    'GuildScheduledEventCreateEvent',
    'GuildScheduledEventDeleteEvent',
    'GuildScheduledEventUpdateEvent',
    'GuildScheduledEventUserAddEvent',
    'GuildScheduledEventUserRemoveEvent',
)


class GuildScheduledEventCreateEvent(GatewayEvent, ScheduledEventResponse):
    """Sent when a guild scheduled event is created.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-create
    """


class GuildScheduledEventUpdateEvent(GatewayEvent, ScheduledEventResponse):
    """Sent when a guild scheduled event is updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-update
    """


class GuildScheduledEventDeleteEvent(GatewayEvent, ScheduledEventResponse):
    """Sent when a guild scheduled event is deleted.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-delete
    """


class GuildScheduledEventUserAddEvent(GatewayEvent, ScheduledEventResponse):
    """Represents a GuildScheduledEventUserAddEvent.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-add-guild-scheduled-event-user-add-event-fields
    """

    guild_scheduled_event_id: Snowflake
    """Guild id scheduled event."""

    user_id: Snowflake
    """User id."""

    guild_id: Snowflake
    """Guild id."""


class GuildScheduledEventUserRemoveEvent(GatewayEvent):
    """Sent when a user has unsubscribed from a guild scheduled event.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-remove-guild-scheduled-event-user-remove-event-fields
    """

    guild_scheduled_event_id: Snowflake
    """Guild id scheduled event."""

    user_id: Snowflake
    """User id."""

    guild_id: Snowflake
    """Guild id."""
