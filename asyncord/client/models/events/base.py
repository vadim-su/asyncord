from __future__ import annotations

from typing import NamedTuple

from pydantic import Field, BaseModel

from asyncord.snowflake import Snowflake
from asyncord.client.models.users import User
from asyncord.client.models.guilds import UnavailableGuild
from asyncord.client.models.applications import ApplicationFlag


class GatewayEvent(BaseModel):
    pass


class HelloEvent(GatewayEvent):
    """https://discord.com/developers/docs/topics/gateway#hello"""

    heartbeat_interval: int
    """the interval (in milliseconds) the client should heartbeat with"""


class ReadyEvent(GatewayEvent):
    api_version: int = Field(alias='v')
    """gateway protocol version"""

    user: User
    """user object"""

    guilds: list[UnavailableGuild]
    """array of unavailable guild objects"""

    session_id: str
    """used for resuming connections"""

    resume_gateway_url: str
    """The gateway url to use for resuming connections."""

    shard: Shard | None = None
    """the shard information associated with this session, if sent when identifying"""

    application: ReadyEventApplication
    """application object"""


class Shard(NamedTuple):
    shard_id: int
    num_shards: int


class ReadyEventApplication(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#ready-ready-event-fields"""

    id: Snowflake
    """the id of the application"""

    flags: ApplicationFlag
    """the application's flags"""


ReadyEvent.update_forward_refs()
