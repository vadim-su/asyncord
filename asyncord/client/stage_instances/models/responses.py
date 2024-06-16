"""Models for StageInstance responses."""

from pydantic import BaseModel

from asyncord.client.stage_instances.models.common import StageInstancePrivacyLevel
from asyncord.snowflake import Snowflake

__all__ = ('StageInstanceResponse',)


class StageInstanceResponse(BaseModel):
    """Represents a StageInstance response.

    Reference:
    https://discord.com/developers/docs/resources/stage-instance#stage-instance-object-stage-instance-structure
    """

    id: Snowflake
    """Id of this Stage instance."""

    guild_id: Snowflake
    """Guild id of the associated Stage channel."""

    channel_id: Snowflake
    """Id of the associated Stage channel."""

    topic: str
    """Topic of the Stage instance. 1-120 characters."""

    privacy_level: StageInstancePrivacyLevel = StageInstancePrivacyLevel.GUILD_ONLY
    """Privacy level of the Stage instance."""

    guild_scheduled_event_id: Snowflake | None = None
    """Id of the scheduled event for this Stage instance."""
