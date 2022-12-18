import datetime

from asyncord.snowflake import Snowflake
from asyncord.client.models.users import User
from asyncord.gateway.events.base import GatewayEvent
from asyncord.client.models.invites import InviteTargetType
from asyncord.client.models.applications import Application


class InviteCreateEvent(GatewayEvent):
    """Sent when a new invite to a channel is created.

    https://discord.com/developers/docs/topics/gateway-events#invite-create
    """

    channel_id: Snowflake
    """Channel the invite is for."""

    code: str
    """Unique invite [code](https://discord.com/developers/docs/resources/invite#invite-object)."""

    created_at: datetime.datetime
    """Time at which the invite was created."""

    guild_id: Snowflake | None = None
    """Guild id of the invite."""

    inviter: User
    """User who created the invite."""

    max_age: int
    """How long the invite is valid for (in seconds).

    0 if it doesn't expire.
    """

    max_uses: int
    """Maximum number of times the invite can be used.

    0 if there is no limit.
    """

    target_type: InviteTargetType | None = None
    """Type of target for the voice channel invite."""

    target_user: User | None = None
    """User whose stream to display for this invite."""

    # FIXME: There is should be a partial application object, but it is not documented
    target_application: Application | None = None
    """Embedded application to open for this voice channel embedded application invite."""

    temporary: bool
    """Whether the invite is temporary.

    Invited users will be kicked on disconnect unless they're assigned a role.
    """

    # TODO: WTF? Why is this always 0?
    uses: int
    """Number of times the invite has been used.

    Always will be 0!
    """


class InviteDeleteEvent(GatewayEvent):
    """Sent when an invite is deleted.

    https://discord.com/developers/docs/topics/gateway-events#invite-delete
    """

    channel_id: Snowflake
    """Channel of the invite."""

    guild_id: Snowflake | None = None
    """Guild of the invite."""

    code: str
    """Unique invite [code](https://discord.com/developers/docs/resources/invite#invite-object)."""
