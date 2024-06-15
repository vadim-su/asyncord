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

    GUILD_SUBSCRIPTION = 'guild_subscription'
    """Guild subscription integration."""


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


@enum.unique
class AuditLogEvents(enum.IntEnum):
    """Audit log events.

    Reference:
    https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-audit-log-events
    """

    GUILD_UPDATE = 1
    """Server settings were updated.

    Object changed: Guild.
    """

    CHANNEL_CREATE = 10
    """Channel was created.

    Object changed: Channel.
    """

    CHANNEL_UPDATE = 11
    """Channel settings were updated.

    Object changed: Channel.
    """

    CHANNEL_DELETE = 12
    """Channel was deleted.

    Object changed: Channel.
    """

    CHANNEL_OVERWRITE_CREATE = 13
    """Permission overwrite was added to a channel.

    Object changed: Channel Overwrite.
    """

    CHANNEL_OVERWRITE_UPDATE = 14
    """Permission overwrite was updated for a channel.

    Object changed: Channel Overwrite.
    """

    CHANNEL_OVERWRITE_DELETE = 15
    """Permission overwrite was deleted from a channel.

    Object changed: Channel Overwrite.
    """

    MEMBER_KICK = 20
    """Member was removed from server."""

    MEMBER_PRUNE = 21
    """Members were pruned from server."""

    MEMBER_BAN_ADD = 22
    """Member was banned from server."""

    MEMBER_BAN_REMOVE = 23
    """Server ban was lifted for a member."""

    MEMBER_UPDATE = 24
    """Member was updated in server.

    Object changed:  Member.
    """

    MEMBER_ROLE_UPDATE = 25
    """Member was added or removed from a role Partial Role *."""

    MEMBER_MOVE = 26
    """Member was moved to a different voice channel."""

    MEMBER_DISCONNECT = 27
    """Member was disconnected from a voice channel."""

    BOT_ADD = 28
    """Bot user was added to server."""

    ROLE_CREATE = 30
    """Role was created.

    Object changed: Role.
    """
    ROLE_UPDATE = 31
    """Role was edited.

    Object changed: Role.
    """
    ROLE_DELETE = 32
    """Role was deleted.

    Object changed: Role.
    """
    INVITE_CREATE = 40
    """Server invite was created

    Object changed: Invite and Invite Metadata *.
    """

    INVITE_UPDATE = 41
    """Server invite was updated

    Object changed: Invite and Invite Metadata *.
    """

    INVITE_DELETE = 42
    """Server invite was deleted.

    Object changed: Invite and Invite Metadata *.
    """

    WEBHOOK_CREATE = 50
    """Webhook was created.

    Object changed: Webhook *.
    """

    WEBHOOK_UPDATE = 51
    """Webhook properties or channel were updated.

    Object changed: Webhook *.
    """

    WEBHOOK_DELETE = 52
    """Webhook was deleted.

    Object changed: Webhook *.
    """

    EMOJI_CREATE = 60
    """Emoji was created.

    Object changed: Emoji.
    """

    EMOJI_UPDATE = 61
    """Emoji name was updated.

    Object changed: Emoji.
    """

    EMOJI_DELETE = 62
    """Emoji was deleted.

    Object changed: Emoji.
    """

    MESSAGE_DELETE = 72
    """Single message was deleted."""

    MESSAGE_BULK_DELETE = 73
    """Multiple messages were deleted."""

    MESSAGE_PIN = 74
    """Message was pinned to a channel."""

    MESSAGE_UNPIN = 75
    """Message was unpinned from a channel."""

    INTEGRATION_CREATE = 80
    """App was added to server.

    Object changed: Integration.
    """

    INTEGRATION_UPDATE = 81
    """App was updated(as an example, its scopes were updated).

    Object changed: Integration.
    """

    INTEGRATION_DELETE = 82
    """App was removed from server.

    Object changed: Integration.
    """

    STAGE_INSTANCE_CREATE = 83
    """Stage instance was created(stage channel becomes live).

    Object changed: Stage Instance.
    """

    STAGE_INSTANCE_UPDATE = 84
    """Stage instance details were updated.

    Object changed: Stage Instance.
    """

    STAGE_INSTANCE_DELETE = 85
    """Stage instance was deleted(stage channel no longer live).

    Object changed: Stage Instance.
    """

    STICKER_CREATE = 90
    """Sticker was created.

    Object changed: Sticker.
    """

    STICKER_UPDATE = 91
    """Sticker details were updated.

    Object changed: Sticker.
    """

    STICKER_DELETE = 92
    """Sticker was deleted.

    Object changed: Sticker.
    """

    GUILD_SCHEDULED_EVENT_CREATE = 100
    """Event was created.

    Object changed: Guild Scheduled Even.
    """

    GUILD_SCHEDULED_EVENT_UPDATE = 101
    """Event was updated.

    Object changed: Guild Scheduled Even.
    """

    GUILD_SCHEDULED_EVENT_DELETE = 102
    """Event was cancelled.

    Object changed: Guild Scheduled Even.
    """

    THREAD_CREATE = 110
    """Thread was created in a channel.

    Object changed: Thread.
    """

    THREAD_UPDATE = 111
    """Thread was updated.

    Object changed: Thread.
    """

    THREAD_DELETE = 112
    """Thread was deleted.

    Object changed: Thread.
    """

    APPLICATION_COMMAND_PERMISSION_UPDATE = 121
    """Permissions were updated for a command.

    Object changed: Command Permission *.
    """

    AUTO_MODERATION_RULE_CREATE = 140
    """Auto Moderation rule was created.

    Object changed: Auto Moderation Rule.
    """

    AUTO_MODERATION_RULE_UPDATE = 141
    """Auto Moderation rule was updated.

    Object changed: Auto Moderation Rule.
    """

    AUTO_MODERATION_RULE_DELETE = 142
    """Auto Moderation rule was deleted.

    Object changed: Auto Moderation Rule.
    """

    AUTO_MODERATION_BLOCK_MESSAGE = 143
    """Message was blocked by Auto Moderation."""

    AUTO_MODERATION_FLAG_TO_CHANNEL = 144
    """Message was flagged by Auto Moderation."""

    AUTO_MODERATION_USER_COMMUNICATION_DISABLED = 145
    """Member was timed out by Auto Moderation."""

    CREATOR_MONETIZATION_REQUEST_CREATED = 150
    """Creator monetization request was created."""

    CREATOR_MONETIZATION_TERMS_ACCEPTED = 151
    """Creator monetization terms were accepted."""


@enum.unique
class WidgetStyleOptions(enum.StrEnum):
    """Widget style options."""

    SHIELD = 'shield'
    """Shield style widget.

    With Discord icon and guild members online count.
    """

    BANNER_1 = 'banner1'
    """Large image with guild icon, name and online count.

    "POWERED BY DISCORD" as the footer of the widget.
    """

    BANNER_2 = 'banner2'
    """Smaller widget style.

    With guild icon, name and online count. Split on the right with Discord logo.
    """

    BANNER_3 = 'banner3'
    """Large image.

    With guild icon, name and online count.
    In the footer, Discord logo on the left and "Chat Now" on the right.
    """

    BANNER_4 = 'banner4'
    """Large Discord logo at the top of the widget.

    Guild icon, name and online count in the middle portion of the widget.
    And a "JOIN MY SERVER" button at the bottom.
    """


@enum.unique
class OnboardingMode(enum.IntEnum):
    """Onboarding mode.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-mode
    """

    ONBOARDING_DEFAULT = 0
    """	Counts only Default Channels towards constraints"""

    ONBOARDING_ADVANCED = 1
    """Counts Default Channels and Questions towards constraints."""


@enum.unique
class OnboardingPromptType(enum.IntEnum):
    """Onboarding prompt types.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-onboarding-object-prompt-types
    """

    MULTIPLE_CHOICE = 0

    DROPDOWN = 1
