"""Presence related events."""

from __future__ import annotations

from pydantic import BaseModel

from asyncord.client.members.models.responses import MemberResponse
from asyncord.client.models.activities import ActivityResponse
from asyncord.client.users.models.responses import UserResponse
from asyncord.gateway.events.base import GatewayEvent
from asyncord.snowflake import Snowflake

__all__ = (
    'ActivityResponse',
    'ClientStatus',
    'PresenceUpdateEvent',
    'TypingStartEvent',
    'UserUpdateEvent',
)


class ClientStatus(BaseModel):
    """Active sessions are indicated with an 'online', 'idle', or 'dnd' string per platform.

    If a user is offline or invisible, the corresponding field is not present.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#client-status-object
    """

    desktop: str | None = None
    """User's status set for an active desktop (Windows, Linux, Mac) application session."""

    mobile: str | None = None
    """User's status set for an active mobile (iOS, Android) application session."""

    web: str | None = None
    """User's status set for an active web (browser, bot account) application session."""


class PresenceUpdateUser(BaseModel):
    """User object sent in presence update events.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#presence-update-presence-update-event-fields
    """

    id: Snowflake
    """User id."""

    username: str | None = None
    """User's username.

    Not unique across the platform.
    """

    discriminator: str | None = None
    """User's 4 - digit discord-tag or 0 if the user has no tag."""

    avatar: str | None = None
    """User's avatar hash."""

    bot: bool | None = None
    """Whether the user belongs to an OAuth2 application."""

    system: bool | None = None
    """Whether the user is an Official Discord System user (part of the urgent message system)."""

    mfa_enabled: bool | None = None
    """Whether the user has two factor enabled on their account."""

    locale: str | None = None
    """User's chosen language option."""

    verified: bool | None = None
    """Whether the email on this account has been verified."""

    email: str | None = None
    """User's email."""

    flags: int | None = None
    """Flags on a user's account."""

    premium_type: int | None = None
    """Type of Nitro subscription on a user's account."""

    public_flags: int | None = None
    """Public flags on a user's account."""


class PresenceUpdateEvent(GatewayEvent):
    """Sent when a user's presence or info, such as name or avatar, is updated.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#presence-update
    """

    user: PresenceUpdateUser
    """the user presence is being updated for

    The user object within this event can be partial, the only field which
    must be sent is the id field, everything else is optional. Along with this
    limitation, no fields are required, and the types of the fields are not validated.
    Your client should expect any combination of fields and types within this event.
    """

    guild_id: Snowflake
    """Guild id."""

    status: str
    """Presence status."""

    activities: list[ActivityResponse]
    """User's current activities."""

    client_status: ClientStatus
    """User's platform-dependent status."""


class TypingStartEvent(GatewayEvent):
    """Sent when a user starts typing in a channel.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#typing-start
    """

    channel_id: Snowflake
    """Channel id."""

    guild_id: Snowflake | None = None
    """Guild id."""

    user_id: Snowflake
    """User id."""

    timestamp: int
    """Unix time (in seconds) of when the user started typing."""

    member: MemberResponse | None = None
    """Member who started typing if this happened in a guild."""


class UserUpdateEvent(GatewayEvent, UserResponse):
    """Sent when properties about the user change.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#user-update
    """
