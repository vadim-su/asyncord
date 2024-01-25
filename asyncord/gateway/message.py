"""Gateway message models."""

import enum
from typing import Annotated, Any, Literal

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel, Field, TypeAdapter


@enum.unique
class GatewayCommandOpcode(enum.IntEnum):
    """Gateway command opcodes."""

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
class GatewayMessageOpcode(enum.IntEnum):
    """Gateway message opcodes."""

    DISPATCH = 0
    """An event was dispatched."""

    RECONNECT = 7
    """You should attempt to reconnect and resume immediately."""

    INVALID_SESSION = 9
    """The session has been invalidated. You should reconnect."""

    HELLO = 10
    """Sent immediately after connecting, contains the heartbeat_interval to use."""

    HEARTBEAT_ACK = 11
    """Sent in response to receiving a heartbeat to acknowledge that it has been received."""


class BaseGatewayMessage(BaseModel):
    """Base gateway message model."""

    opcode: GatewayMessageOpcode = Field(alias='op')
    """Message opcode."""

    data: Any = Field(alias='d')
    """Message data."""

    trace: Any = Field(default=None, alias='_trace')
    """Message trace information."""


class DispatchMessage(BaseGatewayMessage):
    """Dispatch message model."""

    opcode: Literal[GatewayMessageOpcode.DISPATCH] = Field(GatewayMessageOpcode.DISPATCH, alias='op')
    """Message opcode."""

    data: Any = Field(alias='d')
    """Message data.

    We do not parse this data before we were dispatching it to the event handler.
    If user didn't register an event handler for this event, we will not parse it.
    """

    sequence_number: int = Field(alias='s')
    """Sequence number of the message.

    This is used for resuming sessions and heartbeats.
    """

    event_name: str = Field(alias='t')
    """Name of the event.

    This is used to determine which event handler to call and also used for data validation.
    """


class HelloMessageData(BaseModel):
    """Hello message data."""

    heartbeat_interval: int = Field(alias='heartbeat_interval')
    """Interval (in milliseconds) the client should heartbeat with."""


class HelloMessage(BaseGatewayMessage):
    """Hello message model."""

    opcode: Literal[GatewayMessageOpcode.HELLO] = Field(GatewayMessageOpcode.HELLO, alias='op')
    """Message opcode."""

    data: HelloMessageData = Field(alias='d')
    """Hello message data."""


class InvalidSessionMessage(BaseGatewayMessage):
    """Invalid session message model."""

    opcode: Literal[GatewayMessageOpcode.INVALID_SESSION] = Field(GatewayMessageOpcode.INVALID_SESSION, alias='op')
    """Message opcode."""

    data: bool = Field(alias='d')
    """Whether the session can be resumed."""


class DatalessMessage(BaseGatewayMessage):
    """Other gateway messages that do not have data."""


class FallbackGatewayMessage(BaseGatewayMessage):
    """Gateway message model."""

    opcode: Annotated[GatewayMessageOpcode, FallbackAdapter] = Field(alias='op')
    data: Any = Field(alias='d')


# fmt: off
type GatewayMessageType = Annotated[
    DispatchMessage | HelloMessage | InvalidSessionMessage,
    Field(discriminator='opcode'),
] | DatalessMessage | FallbackGatewayMessage
"""Gateway message type."""
# fmt: on

GatewayMessageAdapter: TypeAdapter[GatewayMessageType] = TypeAdapter(GatewayMessageType)
"""Gateway message type adapter."""
