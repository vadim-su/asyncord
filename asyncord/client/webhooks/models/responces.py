"""Contains the responce models for the webhooks resource.."""

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel

from asyncord.client.users.models.responses import UserResponse
from asyncord.client.webhooks.models.common import WebhookType
from asyncord.snowflake import Snowflake

__all__ = (
    'SourceChannel',
    'SourceGuild',
    'WebhookResponse',
)


class SourceGuild(BaseModel):
    """Partial model for guild object.

    Reference:
    https://discord.com/developers/docs/resources/webhook#webhook-object-example-channel-follower-webhook
    """

    id: Snowflake | None = None
    """ID of the guild."""

    name: str | None = None
    """Name of the guild."""

    icon: str | None = None
    """Icon hash of the guild."""


class SourceChannel(BaseModel):
    """Partial model for channel object.

    Reference:
    https://discord.com/developers/docs/resources/webhook#webhook-object-example-channel-follower-webhook
    """

    id: Snowflake | None = None
    """ID of the channel."""

    name: str | None = None
    """Name of the channel."""


class WebhookResponse(BaseModel):
    """Model for webhook response.

    Reference:
    https://discord.com/developers/docs/resources/webhook#webhook-object
    """

    id: Snowflake
    """ID of the webhook."""

    type: FallbackAdapter[WebhookType]
    """Type of the webhook."""

    guild_id: Snowflake | None = None
    """ID of the guild this webhook is for, if any."""

    channel_id: Snowflake | None = None
    """ID of the channel this webhook is for, if any."""

    user: UserResponse | None = None
    """The user this webhook was created by.

    (not returned when getting a webhook with its token).
    """

    name: str | None = None
    """Default name of the webhook."""

    avatar: str | None = None
    """Default user avatar hash of the webhook."""

    token: str | None = None
    """The secure token of the webhook.

    Returned only for incoming webhook type.
    """

    application_id: Snowflake | None = None
    """Bot/OAuth2 application that created this webhook."""

    source_guild: SourceGuild | None = None
    """Guild of the channel that this webhook is following."""

    source_channel: SourceChannel | None = None

    url: str | None = None
    """The url used for executing the webhook.

    (returned by the webhooks OAuth2 flow).
    """
