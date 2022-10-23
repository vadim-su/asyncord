import datetime

from asyncord.snowflake import Snowflake
from asyncord.client.models.users import User
from asyncord.client.models.invites import InviteTargetType
from asyncord.gateway.events.base import GatewayEvent
from asyncord.client.models.applications import Application


class InviteCreateEvent(GatewayEvent):
    """Sent when a new invite to a channel is created.

    https://discord.com/developers/docs/topics/gateway#invite-create
    """

    channel_id: Snowflake
    """the channel the invite is for"""

    code: str
    """the unique invite[code](https://discord.com/developers/docs/resources/invite#invite-object)"""

    created_at: datetime.datetime
    """the time at which the invite was created"""

    guild_id: Snowflake | None = None
    """	the guild of the invite"""

    inviter: User
    """the user who created the invite"""

    max_age: int
    """how long the invite is valid for (in seconds), or 0 if it doesn't expire"""

    max_uses: int
    """the maximum number of times the invite can be used, or 0 if there is no limit"""

    target_type: InviteTargetType | None = None
    """the type of target for the voice channel invite"""

    target_user: User | None = None
    """the user whose stream to display for this invite"""

    # FIXME: There is should be a partial application object, but it is not documented
    target_application: Application | None = None
    """the embedded application to open for this voice channel embedded application invite"""

    temporary: bool
    """whether the invite is temporary (invited users will be kicked
    on disconnect unless they're assigned a role)
    """

    # TODO: WTF? Why is this always 0?
    uses: int
    """the number of times the invite has been used (always will be 0)"""


class InviteDeleteEvent(GatewayEvent):
    """Sent when an invite is deleted.

    https://discord.com/developers/docs/topics/gateway#invite-delete
    """

    channel_id: Snowflake
    """the channel of the invite"""

    guild_id: Snowflake | None = None
    """the guild of the invite"""

    code: str
    """the unique invite[code](https://discord.com/developers/docs/resources/invite#invite-object)"""
