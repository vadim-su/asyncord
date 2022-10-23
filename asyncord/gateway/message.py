import enum
from typing import Any

from pydantic import Field, BaseModel, validator


@enum.unique
class GatewayCommandOpcode(enum.IntEnum):
    HEARTBEAT = 1
    """Fired periodically by the client to keep the connection alive."""

    IDENTIFY = 2
    """Starts a new session during the initial handshake."""

    PRESENCE_UPDATE = 3
    """Update the client's presence."""

    VOICE_STATE_UPDATE = 4
    """Used to join / leave or move between voice channels."""

    RESUME = 6
    """Resume a previous session that was disconnected."""

    REQUEST_GUILD_MEMBERS = 8
    """Request information about offline guild members in a large guild."""


@enum.unique
class GatewayEventOpcode(enum.IntEnum):
    DISPATCH = 0
    """An event was dispatched."""

    RECONNECT = 7
    """You should attempt to reconnect and resume immediately."""

    INVALID_SESSION = 9
    """The session has been invalidated. You should reconnect and identify / resume accordingly."""

    HELLO = 10
    """Sent immediately after connecting, contains the heartbeat_interval to use."""

    HEARTBEAT_ACK = 11
    """Sent in response to receiving a heartbeat to acknowledge that it has been received."""


class GatewayMessage(BaseModel):
    opcode: GatewayEventOpcode = Field(alias='op')
    msg_data: Any = Field(alias='d')
    sequence_number: int | None = Field(alias='s')
    event_name: str | None = Field(alias='t')
    trace: Any = Field(default=None, alias='_trace')

    @validator('event_name', 'sequence_number')
    def check_values_are_not_none(cls, value, values):  # noqa: N805,WPS110
        if values['opcode'] == GatewayEventOpcode.DISPATCH:
            if value is None:
                raise ValueError('Event name and sequence number must be set')

        elif value is not None:
            raise ValueError('Event name and sequence number must be None')

        return value
