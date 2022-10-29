from __future__ import annotations

import enum
import platform

from pydantic import BaseModel

from asyncord import __version__
from asyncord.gateway.intents import DEFAULT_INTENTS, Intent
from asyncord.client.models.activity import Activity


class IdentifyConnectionProperties(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#identify-identify-connection-properties"""

    os: str = f'{platform.system()} {platform.node()} {platform.release()}'
    """the operating system of the bot"""

    browser: str = f'asyncord-{__version__}'
    """the library name of the bot"""

    device: str = f'asyncord-{__version__}'
    """the library name of the bot"""


class ResumeCommand(BaseModel):
    """Resume a connection to the gateway.

    https://discord.com/developers/docs/topics/gateway-events#resume-resume-structure
    """

    token: str
    """Session token."""

    session_id: str
    """Session ID."""

    seq: int
    """Last sequence number received."""


class IdentifyCommand(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#identify"""

    token: str
    """authentication token"""

    intents: Intent = DEFAULT_INTENTS
    """the gateway intents you wish to receive"""

    presence: PresenceUpdateData | None = None
    """the presence structure for initial presence information"""

    large_threshold: int | None = None
    """value between 50 and 250, total number of members where the gateway
    will stop sending offline members in the guild member list. Defaults to 50"""

    compress: bool | None = None
    """whether this connection supports compression of packets. Defaults to False"""

    shard: tuple[int, int] | None = None
    """used for Guild Sharding"""

    properties: IdentifyConnectionProperties = IdentifyConnectionProperties()
    """connection properties"""


@enum.unique
class StatusType(enum.StrEnum):
    """https://discord.com/developers/docs/topics/gateway#update-presence-status-types"""

    ONLINE = 'online'
    """online"""

    DND = 'dnd'
    """do not disturb"""

    IDLE = 'idle'
    """AFK"""

    INVISIBLE = 'invisible'
    """Invisible and shown as offline"""

    OFFLINE = 'offline'
    """offline"""


class PresenceUpdateData(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#update-presence-gateway-presence-update-structure"""

    since: int | None = None
    """unix time (in milliseconds) of when the client went idle, or null if the client is not idle"""

    activities: list[Activity] | None = None
    """the user's activities"""

    status: StatusType = StatusType.ONLINE
    """the user's new status"""

    afk: bool = False
    """whether or not the client is afk"""


IdentifyCommand.update_forward_refs()
PresenceUpdateData.update_forward_refs()
