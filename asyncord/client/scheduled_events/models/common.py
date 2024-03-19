"""This module contains common enumerations for the scheduled events models."""

import enum


@enum.unique
class EventPrivacyLevel(enum.IntEnum):
    """Represents a scheduled event's privacy level.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-privacy-level
    """

    GUILD_ONLY = 2
    """Scheduled event is private, only available to guild members."""


@enum.unique
class EventStatus(enum.IntEnum):
    """Represents a scheduled event's status.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-status
    """

    SCHEDULED = 1
    """Scheduled event is scheduled."""

    ACTIVE = 2
    """Scheduled event is currently active."""

    COMPLETED = 3
    """Scheduled event has concluded."""

    CANCELED = 4
    """Scheduled event was canceled."""


@enum.unique
class EventEntityType(enum.IntEnum):
    """Represents a scheduled event's entity type.

    Reference:
    https://discord.com/developers/docs/resources/guild-scheduled-event#guild-scheduled-event-object-guild-scheduled-event-entity-types
    """

    STAGE_INSTANCE = 1
    """Scheduled event is associated with a stage instance."""

    VOICE = 2
    """Scheduled event is associated with a voice channel."""

    EXTERNAL = 3
    """Scheduled event is not associated with a guild channel."""
