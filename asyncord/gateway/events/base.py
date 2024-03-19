"""This module defines the base classes for all gateway events in Asyncord.

The gateway is Discord's real-time API for sending and receiving events. These events
are used to notify clients of changes in state, such as when a user sends a message or
when a guild is updated.
"""

from __future__ import annotations

import re
from typing import NamedTuple

from pydantic import BaseModel, Field

from asyncord.client.applications.models.responses import ApplicationFlag
from asyncord.client.users.models.responses import UserResponse
from asyncord.snowflake import Snowflake


class GatewayEvent(BaseModel):
    """Base class for all gateway events."""

    @classmethod
    @property
    def __event_name__(cls) -> str:  # noqa: PLW3201
        """Name of the event.

        Used for identifying the event.
        """
        class_name_without_suffix = cls.__name__[:-5]
        # make camel case into snake case
        event_name = re.sub('(?<!^)(?=[A-Z])', '_', class_name_without_suffix)
        return event_name.upper()


class Shard(NamedTuple):
    """Shard information associated with this session."""

    shard_id: int
    num_shards: int


class ReadyEventApplication(BaseModel):
    """Application object.

    https://discord.com/developers/docs/topics/gateway-events#ready-ready-event-fields
    """

    id: Snowflake
    """the id of the application"""

    flags: ApplicationFlag
    """the application's flags"""


class UnavailableGuild(BaseModel):
    """Unavailable guild object."""

    id: Snowflake
    """Guild ID"""

    unavailable: bool
    """True if this guild is unavailable due to an outage."""


class ReadyEvent(GatewayEvent):
    """Dispatched when a client has successfully connected to the gateway.

    The ready event can be the largest and most complex event the gateway will send,
    as it contains all the state required for a client to begin interacting with
    the rest of the platform.

    https://discord.com/developers/docs/topics/gateway-events#ready
    """

    api_version: int = Field(alias='v')
    """Gateway protocol version."""

    user: UserResponse
    """User object."""

    guilds: list[UnavailableGuild]
    """Array of unavailable guild objects."""

    session_id: str
    """Used for resuming connections."""

    resume_gateway_url: str
    """Gateway url to use for resuming connections."""

    shard: Shard | None = None
    """Shard information associated with this session.

    If sent when identifying.
    """

    application: ReadyEventApplication
    """Application object.

    Contains the application's id and flags.
    """


class ResumedEvent(GatewayEvent):
    """Dispatched when a client has sent a resume payload to the gateway.

    For resuming existing sessions.

    https://discord.com/developers/docs/topics/gateway-events#resume.
    """


class ReconnectEvent(BaseModel):
    """Dispatched when the client should reconnect to the gateway.

    https://discord.com/developers/docs/topics/gateway-events#reconnect
    """


class InvalidSessionEvent(GatewayEvent):
    """Dispatched when the client's session is no longer valid.

    Sent to indicate one of at least three different situations:
    - the gateway could not initialize a session after receiving an Identify event
    - the gateway could not resume a session after receiving a Resume event
    - the gateway has invalidated an active session and is requesting client action

    https://discord.com/developers/docs/topics/gateway-events#invalid-session
    """

    is_resumable: bool
    """Whether or not the session can be resumed."""
