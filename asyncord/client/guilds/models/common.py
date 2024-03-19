"""Common models for guilds."""

import enum


@enum.unique
class DefaultMessageNotificationLevel(enum.IntEnum):
    """Level of default message notifications.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-object-default-message-notification-level
    """

    ALL_MESSAGES = 0
    """Members will receive notifications for all messages by default."""

    ONLY_MENTIONS = 1
    """Members will receive notifications only for messages that @mention them by default."""


@enum.unique
class ExplicitContentFilterLevel(enum.IntEnum):
    """Level of explicit content filter.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-object-explicit-content-filter-level
    """

    DISABLED = 0
    """Media content will not be scanned."""

    MEMBERS_WITHOUT_ROLES = 1
    """Media content sent by members without roles will be scanned."""

    ALL_MEMBERS = 2
    """Media content sent by all members will be scanned."""


@enum.unique
class MFALevel(enum.IntEnum):
    """Level of Multi Factor Authentication."""

    NONE = 0
    """guild has no MFA/2FA requirement for moderation actions"""

    ELEVATED = 1
    """guild has a 2FA requirement for moderation actions"""


@enum.unique
class IntegrationType(enum.StrEnum):
    """Type of integration."""

    TWITCH = 'twitch'
    """Twitch integration."""

    YOUTUBE = 'youtube'
    """YouTube integration."""

    DISCORD = 'discord'
    """Discord integration."""


@enum.unique
class InviteTargetType(enum.IntEnum):
    """The target type of an invite.

    Reference:
    https://discord.com/developers/docs/resources/invite#invite-object-invite-target-types
    """

    STREAM = 1
    """The invite is for a stream."""

    EMBEDDED_APPLICATION = 2
    """The invite is for an embedded application."""


@enum.unique
class ExpireBehaviorOut(enum.IntEnum):
    """Behavior of expiring subscribers."""

    REMOVE_ROLE = 0
    """Remove the role."""

    KICK = 1
    """Kick the user."""
