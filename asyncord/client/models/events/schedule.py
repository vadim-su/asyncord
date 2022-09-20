from asyncord.snowflake import Snowflake
from asyncord.client.models.schedule import GuildScheduleEvent
from asyncord.client.models.events.base import GatewayEvent


class GuildScheduledEventCreateEvent(GatewayEvent, GuildScheduleEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-create"""


class GuildScheduledEventUpdateEvent(GatewayEvent, GuildScheduleEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-update"""


class GuildScheduledEventDeleteEvent(GatewayEvent, GuildScheduleEvent):
    """https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-delete"""


class GuildScheduledEventUserAddEvent(GatewayEvent, GuildScheduleEvent):
    """Represents a GuildScheduledEventUserAddEvent.

    https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-user-add-guild-scheduled-event-user-add-event-fields
    """

    guild_scheduled_event_id: Snowflake
    """id of the guild scheduled event"""

    user_id: Snowflake
    """id of the user"""

    guild_id: Snowflake
    """id of the guild"""


class GuildScheduledEventUserRemoveEvent(GatewayEvent):
    """Sent when a user has unsubscribed from a guild scheduled event.

    https://discord.com/developers/docs/topics/gateway#guild-scheduled-event-user-remove-guild-scheduled-event-user-remove-event-fields
    """

    guild_scheduled_event_id: Snowflake
    """id of the guild scheduled event"""

    user_id: Snowflake
    """id of the user"""

    guild_id: Snowflake
    """id of the guild"""
