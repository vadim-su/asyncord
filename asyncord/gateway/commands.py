"""This module contains the models for the commands sent to the gateway."""

import enum
import platform

from pydantic import BaseModel

from asyncord import __version__
from asyncord.client.models.activities import Activity
from asyncord.gateway.intents import DEFAULT_INTENTS, Intent

__all__ = (
    'IdentifyCommand',
    'IdentifyConnectionProperties',
    'PresenceUpdateData',
    'ResumeCommand',
    'StatusType',
)


class IdentifyConnectionProperties(BaseModel):
    """Identify connection properties.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#identify-identify-connection-properties
    """

    os: str = f'{platform.system()} {platform.node()} {platform.release()}'
    """Operating system of the bot."""

    browser: str = f'asyncord-{__version__}'
    """Library name of the bot."""

    device: str = f'asyncord-{__version__}'
    """Library name of the bot."""


@enum.unique
class StatusType(enum.StrEnum):
    """Possible statuses for a user.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#update-presence-status-types
    """

    ONLINE = 'online'
    """Online"""

    DND = 'dnd'
    """Do not disturb."""

    IDLE = 'idle'
    """AFK."""

    INVISIBLE = 'invisible'
    """Invisible and shown as offline."""

    OFFLINE = 'offline'
    """Offline"""


class PresenceUpdateData(BaseModel):
    """Presence update data.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#update-presence-gateway-presence-update-structure
    """

    since: int | None = None
    """Unix time (in milliseconds) of when the client went idle.

    None if the client is not idle.
    """

    activities: list[Activity] | None = None
    """User's activities."""

    status: StatusType = StatusType.ONLINE
    """User's new status."""

    afk: bool = False
    """Whether or not the client is afk."""


class ResumeCommand(BaseModel):
    """Resume a connection to the gateway.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#resume-resume-structure
    """

    token: str
    """Session token."""

    session_id: str
    """Session ID."""

    seq: int
    """Last sequence number received."""


class IdentifyCommand(BaseModel):
    """Identify a connection to the gateway.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#identify-identify-structure
    """

    token: str
    """Authentication token."""

    intents: Intent = DEFAULT_INTENTS
    """Gateway intents you wish to receive."""

    presence: PresenceUpdateData | None = None
    """Presence structure for initial presence information."""

    large_threshold: int | None = None
    """Total number of members where the gateway will stop sending offline members.

    Defaults to 50.
    """

    compress: bool | None = None
    """Whether this connection supports compression of packets.

    Defaults to False.
    """

    shard: tuple[int, int] | None = None
    """Used for Guild Sharding."""

    properties: IdentifyConnectionProperties = IdentifyConnectionProperties()
    """Connection properties."""
