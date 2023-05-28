from asyncord.client.models.schedule import GuildScheduleEvent
from asyncord.gateway.events.base import GatewayEvent
from asyncord.snowflake import Snowflake


class GuildScheduledEventCreateEvent(GatewayEvent, GuildScheduleEvent):
    """Sent when a guild scheduled event is created.

    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-create
    """


class GuildScheduledEventUpdateEvent(GatewayEvent, GuildScheduleEvent):
    """Sent when a guild scheduled event is updated.

    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-update
    """


class GuildScheduledEventDeleteEvent(GatewayEvent, GuildScheduleEvent):
    """Sent when a guild scheduled event is deleted.

    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-delete
    """


class GuildScheduledEventUserAddEvent(GatewayEvent, GuildScheduleEvent):
    """Represents a GuildScheduledEventUserAddEvent.

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

    https://discord.com/developers/docs/topics/gateway-events#guild-scheduled-event-user-remove-guild-scheduled-event-user-remove-event-fields
    """

    guild_scheduled_event_id: Snowflake
    """Guild id scheduled event."""

    user_id: Snowflake
    """User id."""

    guild_id: Snowflake
    """Guild id."""
