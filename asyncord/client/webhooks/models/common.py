"""Contains the common models for the webhooks resource."""

import enum


@enum.unique
class WebhookType(enum.IntEnum):
    """Type of the webhook.

    Reference:
    https://discord.com/developers/docs/resources/webhook#webhook-object-webhook-types
    """

    INCOMING = 1
    """Incoming Webhooks can post messages to channels with a generated token."""

    CHANNEL_FOLLOWER = 2
    """Internal webhooks used with Channel Following.

    To post new messages into channels.
    """

    APPLICATION = 3
    """Webhooks used with Interactions."""
