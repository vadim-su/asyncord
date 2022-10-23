from __future__ import annotations

from pydantic import BaseModel

from asyncord.snowflake import Snowflake
from asyncord.client.models.users import User
from asyncord.client.models.members import Member
from asyncord.client.models.activity import Activity
from asyncord.gateway.events.base import GatewayEvent


class PresenceUpdateEvent(GatewayEvent):
    """Sent when a user's presence or info, such as name or avatar, is updated.

    https://discord.com/developers/docs/topics/gateway#presence-update
    """

    user: PresenceUpdateUser
    """the user presence is being updated for

    The user object within this event can be partial, the only field which
    must be sent is the id field, everything else is optional. Along with this
    limitation, no fields are required, and the types of the fields are not validated.
    Your client should expect any combination of fields and types within this event.
    """

    guild_id: Snowflake
    """id of the guild"""

    status: str
    """either 'idle', 'dnd', 'online', or 'offline'"""

    activities: list[Activity]
    """user's current activities"""

    client_status: ClientStatus
    """user's platform-dependent status"""


class PresenceUpdateUser(BaseModel):
    """https://discord.com/developers/docs/topics/gateway#presence-update-presence-update-event-fields"""

    id: Snowflake
    """the user's id"""

    username: str | None = None
    """the user's username, not unique across the platform"""

    discriminator: str | None = None
    """the user's 4-digit discord-tag"""

    avatar: str | None = None
    """the user's avatar hash"""

    bot: bool | None = None
    """whether the user belongs to an OAuth2 application"""

    system: bool | None = None
    """whether the user is an Official Discord System user (part of the urgent message system)"""

    mfa_enabled: bool | None = None
    """whether the user has two factor enabled on their account"""

    locale: str | None = None
    """the user's chosen language option"""

    verified: bool | None = None
    """whether the email on this account has been verified"""

    email: str | None = None
    """the user's email"""

    flags: int | None = None
    """the flags on a user's account"""

    premium_type: int | None = None
    """the type of Nitro subscription on a user's account"""

    public_flags: int | None = None
    """the public flags on a user's account"""


class TypingStartEvent(GatewayEvent):
    """Sent when a user starts typing in a channel.

    https://discord.com/developers/docs/topics/gateway#typing-start
    """

    channel_id: Snowflake
    """the id of the channel"""

    guild_id: Snowflake | None = None
    """the id of the guild"""

    user_id: Snowflake
    """the id of the user"""

    timestamp: int
    """unix time (in seconds) of when the user started typing"""

    member: Member | None = None
    """the member who started typing if this happened in a guild"""


class UserUpdateEvent(GatewayEvent, User):
    """Sent when properties about the user change.

    https://discord.com/developers/docs/topics/gateway#user-update
    """


class ClientStatus(BaseModel):
    """Active sessions are indicated with an 'online', 'idle', or 'dnd' string per platform.

    If a user is offline or invisible, the corresponding field is not present.

    https://discord.com/developers/docs/topics/gateway#client-status-object
    """

    desktop: str | None = None
    """the user's status set for an active desktop (Windows, Linux, Mac) application session"""

    mobile: str | None = None
    """the user's status set for an active mobile (iOS, Android) application session"""

    web: str | None = None
    """the user's status set for an active web (browser, bot account) application session"""


PresenceUpdateEvent.update_forward_refs()
