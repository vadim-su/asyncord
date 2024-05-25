"""Models for stage instance resource requests."""

from pydantic import BaseModel, Field

from asyncord.client.stage_instances.models.common import StageInstancePrivacyLevel
from asyncord.snowflake import SnowflakeInputType


class CreateStageInstanceRequest(BaseModel):
    """Model for CreateStageInstance request.

    Reference:
    https://canary.discord.com/developers/docs/resources/stage-instance#create-stage-instance-json-params
    """

    channel_id: SnowflakeInputType
    """Id of the Stage channel."""

    topic: str = Field(None, min_length=1, max_length=120)
    """Topic of the Stage instance. 1-120 characters."""

    privacy_level: StageInstancePrivacyLevel | None = None
    """Privacy level of the Stage instance. Default GUILD_ONLY."""

    send_start_notification: bool | None = None
    """Notify @everyone that a Stage instance has started."""

    guild_scheduled_event_id: SnowflakeInputType | None = None
    """Guild scheduled event associated with the Stage instance."""


class UpdateStageInstanceRequest(BaseModel):
    """Model for Update StageInstance request.

    Reference:
    https://canary.discord.com/developers/docs/resources/stage-instance#modify-stage-instance-json-params
    """

    topic: str | None = Field(None, min_length=1, max_length=120)
    """Topic of the stage instance. 1-120 characters"""

    privacy_level: StageInstancePrivacyLevel | None = None
    """Privacy level of the stage instance."""