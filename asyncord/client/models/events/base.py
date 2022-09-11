from typing import Any

from pydantic import Field, BaseModel

from asyncord.client.models.users import User
from asyncord.client.models.guilds import UnavailableGuild


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

    shard: tuple[int, int] | None = None
    """the shard information associated with this session, if sent when identifying"""

    application: dict[str, Any] | None = None
    """application object"""
