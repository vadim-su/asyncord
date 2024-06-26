"""Response models for guilds."""

import datetime
from typing import Any

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel
from yarl import URL

from asyncord import urls
from asyncord.client.channels.models.common import ChannelType
from asyncord.client.commands.models.responses import ApplicationCommandResponse
from asyncord.client.emojis.models.responses import EmojiResponse
from asyncord.client.guilds.models.common import (
    AuditLogEvents,
    ExpireBehaviorOut,
    IntegrationType,
    InviteTargetType,
    OnboardingMode,
    OnboardingPromptType,
)
from asyncord.client.models.automoderation import AutoModerationRule
from asyncord.client.models.stickers import Sticker
from asyncord.client.roles.models.responses import RoleResponse
from asyncord.client.scheduled_events.models.responses import ScheduledEventResponse
from asyncord.client.threads.models.responses import ThreadResponse
from asyncord.client.users.models.responses import UserResponse
from asyncord.client.webhooks.models.responces import WebhookResponse
from asyncord.snowflake import Snowflake

__all__ = (
    'AuditLogChangeOut',
    'AuditLogEntryOut',
    'AuditLogIntegrationOut',
    'AuditLogResponse',
    'GuildPreviewResponse',
    'GuildResponse',
    'IntegrationAccountOut',
    'IntegrationApplicationOut',
    'IntegrationResponse',
    'InviteChannelOut',
    'InviteGuildOut',
    'InviteResponse',
    'OnboardingPromptOptionOut',
    'OnboardingPromptOut',
    'OnboardingResponse',
    'OptionalAuditLogEntryInfoOut',
    'PruneResponse',
    'VanityUrlInviteResponse',
    'VoiceRegionResponse',
    'WelcomeScreenChannelOut',
    'WelcomeScreenResponse',
    'WidgetChannelResponse',
    'WidgetResponse',
    'WidgetSettingsResponse',
    'WidgetUserResponse',
)


class WelcomeScreenChannelOut(BaseModel):
    """Welcome screen channel object.

    Reference:
    https://discord.com/developers/docs/resources/guild#welcome-screen-object-welcome-screen-channel-structure
    """

    channel_id: Snowflake
    """ID of the channel."""

    description: str
    """Description of the channel."""

    emoji_id: Snowflake | None
    """Emoji ID, if the emoji is custom."""

    emoji_name: str | None
    """Emoji name if custom, the unicode character if standard, or null if no emoji is set."""


class WelcomeScreenResponse(BaseModel):
    """Welcome screen object.

    Reference:
    https://discord.com/developers/docs/resources/guild#welcome-screen-object
    """

    description: str | None
    """Server description shown in the welcome screen."""

    welcome_channels: list[WelcomeScreenChannelOut]
    """List of channels shown in the welcome screen."""


class GuildResponse(BaseModel):
    """Guild object.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-object
    """

    id: Snowflake
    """Guild ID."""

    name: str
    """Guild name.

    Should be between 2 and 100 characters excluding trailing and leading whitespace.
    """

    icon: str | None = None
    """Guild icon hash."""

    icon_hash: str | None = None
    """Icon hash, returned when in the template object."""

    splash: str | None
    """Splash hash."""

    discovery_splash: str | None
    """Discovery splash hash, only present for guilds with the "DISCOVERABLE" feature."""

    owner: bool | None = None
    """True if the user is the owner of the guild."""

    owner_id: Snowflake
    """ID of owner."""

    permissions: str | None = None
    """Total permissions for the user in the guild (excludes overwrites)."""

    region: str | None = None
    """Voice region ID for the guild (deprecated)."""

    afk_channel_id: Snowflake | None = None
    """ID of AFK channel."""

    afk_timeout: int
    """AFK timeout in seconds."""

    widget_enabled: bool | None = None
    """True if the server widget is enabled."""

    widget_channel_id: Snowflake | None = None
    """Channel ID that the widget will generate an invite to, or null if set to no invite."""

    verification_level: int
    """Verification level required for the guild."""

    default_message_notifications: int
    """Default message notifications level."""

    explicit_content_filter: int
    """Explicit content filter level."""

    roles: list[RoleResponse] | None = None
    """Roles in the guild."""

    emojis: list[EmojiResponse] | None = None
    """Custom guild emojis."""

    features: list[str]
    """Allowed guild features.

    Replaced by str because it often changes without any notifications.
    """

    mfa_level: int
    """Required MFA level for the guild."""

    application_id: Snowflake | None
    """Application ID of the guild creator if it is bot-created."""

    system_channel_id: Snowflake | None
    """ID of the channel where guild notices such as welcome messages and boost events are posted."""

    system_channel_flags: int
    """System channel flags."""

    rules_channel_id: Snowflake | None
    """ID of the channel where Community guilds can display rules and/or guidelines."""

    max_presences: int | None = None
    """Maximum number of presences for the guild (null is always returned, apart from the largest of guilds)."""

    max_members: int
    """Maximum number of members for the guild."""

    vanity_url_code: str | None
    """Vanity URL code for the guild."""

    description: str | None
    """Guild description (0-1000 characters)."""

    banner: str | None
    """Guild banner hash."""

    premium_tier: int
    """Premium tier (Server Boost level)."""

    premium_subscription_count: int
    """Number of boosts this guild currently has."""

    preferred_locale: str
    """Preferred locale of a Community guild used in server discovery and notices

    Sent in interactions. Defaults to "en-US".
    """

    public_updates_channel_id: Snowflake | None
    """ID of the channel where admins and moderators of Community guilds receive notices from Discord."""

    max_video_channel_users: int | None = None
    """Maximum amount of users in a video channel."""

    max_stage_video_channel_users: int | None = None
    """Maximum amount of users in a stage video channel."""

    approximate_member_count: int | None = None
    """Approximate number of members in this guild.

    Returned from the GET /guilds/<id> endpoint when with_counts is true.
    """

    approximate_presence_count: int | None = None
    """Approximate number of non-offline members in this guild.

    Returned when with_counts is true.
    """

    welcome_screen: WelcomeScreenResponse | None = None
    """Welcome screen of a Community guild.

    Shown to new members, returned in an Invite's guild object.
    """

    nsfw_level: int
    """Guild NSFW level."""

    stickers: list[Sticker] | None = None
    """custom guild stickers"""

    premium_progress_bar_enabled: bool
    """Whether the guild has the boost progress bar enabled."""

    safety_alerts_channel_id: Snowflake | None
    """ID of the channel where admins and moderators of Community guilds receive safety alerts from Discord."""


class GuildPreviewResponse(BaseModel):
    """Guild preview object.

    https://discord.com/developers/docs/resources/guild#guild-preview-object
    """

    id: Snowflake
    """Guild ID."""

    name: str
    """Guild name.

    2 - 100 characters, excluding trailing and leading whitespace.
    """

    icon: str | None
    """Icon hash."""

    splash: str | None
    """Splash hash."""

    discovery_splash: str | None
    """Discovery splash hash.

    Only present for guilds with the "DISCOVERABLE" feature.
    """

    emojis: list[EmojiResponse] | None = None
    """Custom guild emojis."""

    features: list[str]
    """Enabled guild features.

    Replaced by str because too often changes without any notifications.
    """

    approximate_member_count: int | None = None
    """Approximate number of members in this guild."""

    approximate_presence_count: int | None = None
    """Approximate number of non - offline members in this guild."""

    description: str | None = None
    """Description for the guild, if the guild is discoverable."""

    stickers: list[Sticker] | None = None
    """Custom guild stickers"""


class PruneResponse(BaseModel):
    """Prune object.

    Reference:
    https://discord.com/developers/docs/resources/guild#get-guild-prune-count
    """

    pruned: int | None
    """Number of members pruned."""


class VoiceRegionResponse(BaseModel):
    """Voice region object.

    Reference:
    https://discord.com/developers/docs/resources/voice#voice-region-object-voice-region-structure
    """

    id: str
    """Voice region id."""

    name: str
    """Voice region name."""

    optimal: bool
    """Whether the voice region is optimal for voice communication."""

    deprecated: bool
    """Whether the voice region is deprecated."""

    custom: bool
    """Whether the voice region is custom."""


class InviteChannelOut(BaseModel):
    """Invite channel object.

    Reference:
    https://discord.com/developers/docs/resources/invite#invite-object-example-invite-object
    """

    id: Snowflake
    """Channel id."""

    name: str
    """Channel name."""

    type: FallbackAdapter[ChannelType]
    """Type of channel."""


class InviteGuildOut(BaseModel):
    """Invite guild object.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-object
    https://discord.com/developers/docs/resources/invite#invite-object-example-invite-object
    """

    id: str
    """Guild ID."""

    name: str
    """Guild name.

    Should be between 2 and 100 characters excluding trailing and leading whitespace.
    """

    icon: str | None = None
    """Icon hash."""

    splash: str | None
    """Splash hash."""

    features: list[str]
    """Allowed guild features.

    Replaced by str because too often changes without any notifications.
    """

    description: str | None
    """Guild description.

    Characters count should be between 0 and 1000.
    """

    banner: str | None
    """Guild banner hash."""

    verification_level: int
    """Guild verification level."""

    vanity_url_code: str | None
    """Guild vanity URL code."""

    nsfw_level: int
    """Guild NSFW level."""

    premium_subscription_count: int
    """Number of boosts this guild currently has."""


class InviteResponse(BaseModel):
    """Invite object.

    Reference:
    https://discord.com/developers/docs/resources/invite#invite-object-invite-structure
    """

    code: str
    """Unique identifier for the invite."""

    guild: InviteGuildOut | None = None
    """Guild the invite is for."""

    channel: InviteChannelOut | None
    """channel the invite is for"""

    inviter: UserResponse | None = None
    """user who created the invite"""

    target_type: FallbackAdapter[InviteTargetType] | None = None
    """Type of target for this voice channel invite."""

    target_user: UserResponse | None = None
    """User whose stream to display for this voice channel stream invite."""

    # TODO: Add target_application specific type
    target_application: dict[str, Any] | None = None
    """Application to open for this voice channel embedded application invite."""

    approximate_presence_count: int | None = None
    """Approximate count of online members.

    Return from get_invite endpoint only when `with_counts` is True.
    """

    approximate_member_count: int | None = None
    """Approximate count of total members.

    Return from get_invite endpoint only when `with_counts` is True.
    """

    expires_at: datetime.datetime | None = None
    """When this invite expires.

    Return from get_invite endpoint only when `with_expiration` is True.
    """

    guild_scheduled_event: ScheduledEventResponse | None = None
    """Guild scheduled event.

    Return from get_invite endpoint only when `guild_scheduled_event_id` is not None
    and contains a valid id.
    """

    @property
    def url(self) -> URL:
        """Invite URL."""
        return urls.INVITE_BASE_URL / self.code


class IntegrationAccountOut(BaseModel):
    """Integration Account Structure.

    Reference:
    https://discord.com/developers/docs/resources/guild#integration-account-object
    """

    id: str
    """ID of the account."""

    name: str
    """Name of the account."""


class IntegrationApplicationOut(BaseModel):
    """Integration Application Structure.

    Reference:
    https://discord.com/developers/docs/resources/guild#integration-application-object
    """

    id: Snowflake
    """ID of the app."""

    name: str
    """Name of the app."""

    icon: str | None = None
    """Icon hash of the app"""

    description: str
    """Description of the app."""

    bot: UserResponse | None = None
    """Bot associated with this application."""


class IntegrationResponse(BaseModel):
    """Inntegration object.

    Reference:
    https://discord.com/developers/docs/resources/guild#integration-object-integration-structure
    """

    id: Snowflake
    """Integration id."""

    name: str
    """Integration name."""

    type: FallbackAdapter[IntegrationType]
    """Integration type (twitch, youtube, or discord)."""

    enabled: bool
    """Is this integration enabled."""

    syncing: bool | None = None
    """Is this integration being synced."""

    role_id: Snowflake | None = None
    """ID that this integration uses for "subscribers."""

    enable_emoticons: bool | None = None
    """Whether emoticons should be synced for this integration (twitch only currently)."""

    expire_behavior: FallbackAdapter[ExpireBehaviorOut] | None = None
    """Behavior of expiring subscribers."""

    expire_grace_period: int | None = None
    """Grace period (in days) before expiring subscribers."""

    user: UserResponse
    """User for this integration."""

    account: IntegrationAccountOut
    """Integration account information."""

    synced_at: datetime.datetime | None = None
    """When this integration was last synced."""

    subscriber_count: int | None = None
    """How many subscribers this integration has."""

    revoked: bool | None = None
    """Has this integration been revoked."""

    application: IntegrationApplicationOut | None = None
    """Bot or OAuth2 application for discord integrations."""

    scopes: list[str] | None = None
    """Scopes the application has been authorized for."""


class AuditLogIntegrationOut(BaseModel):
    """Partial integration object.

    Reference:
    https://discord.com/developers/docs/resources/audit-log#audit-log-object-example-partial-integration-object
    """

    id: Snowflake
    """Integration id."""

    name: str
    """Integration name."""

    type: FallbackAdapter[IntegrationType]
    """Integration type (twitch, youtube, or discord)."""

    account: IntegrationAccountOut
    """Integration account information."""

    application_id: Snowflake
    """Application id."""


class AuditLogChangeOut(BaseModel):
    """Audit log change object.

    Reference:
    https://discord.com/developers/docs/resources/audit-log#audit-log-change-object-audit-log-change-structure
    """

    new_value: Any | None = None
    """New value of the key."""

    old_value: Any | None = None
    """Old value of the key."""

    key: str
    """Name of the changed entity, with a few exceptions.

    Exceptions:
    https://discord.com/developers/docs/resources/audit-log#audit-log-change-object-audit-log-change-exceptions
    """


class OptionalAuditLogEntryInfoOut(BaseModel):
    """Audit log entry info object.

    Reference:
    https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-optional-audit-entry-info
    """

    application_id: Snowflake | None = None
    """ID of the app whose permissions were targeted.

    APPLICATION_COMMAND_PERMISSION_UPDATE.
        """

    auto_moderation_rule_name: str | None = None
    """Name of the Auto Moderation rule that was triggered.

    AUTO_MODERATION_BLOCK_MESSAGE & AUTO_MODERATION_FLAG_TO_CHANNEL
        & AUTO_MODERATION_USER_COMMUNICATION_DISABLED.
        """

    auto_moderation_rule_trigger_type: str | None = None
    """Trigger type of the Auto Moderation rule that was triggered.

    AUTO_MODERATION_BLOCK_MESSAGE & AUTO_MODERATION_FLAG_TO_CHANNEL
        & AUTO_MODERATION_USER_COMMUNICATION_DISABLED.
        """

    channel_id: Snowflake | None = None
    """Channel in which the entities were targeted.

    MEMBER_MOVE & MESSAGE_PIN & MESSAGE_UNPIN & MESSAGE_DELETE
    & STAGE_INSTANCE_CREATE & STAGE_INSTANCE_UPDATE & STAGE_INSTANCE_DELETE
    & AUTO_MODERATION_BLOCK_MESSAGE & AUTO_MODERATION_FLAG_TO_CHANNEL
    & AUTO_MODERATION_USER_COMMUNICATION_DISABLED.
    """

    count: str | None = None
    """Number of entities that were targeted.

    MESSAGE_DELETE & MESSAGE_BULK_DELETE & MEMBER_DISCONNECT & MEMBER_MOVE.
    """

    delete_member_days: str | None = None
    """Number of days after which inactive members were kicked.

    MEMBER_PRUNE.
    """

    id: Snowflake | None = None
    """ID of the overwritten entity.

    CHANNEL_OVERWRITE_CREATE & CHANNEL_OVERWRITE_UPDATE & CHANNEL_OVERWRITE_DELETE.
    """

    members_removed: str | None = None
    """Number of members removed by the prune.

    MEMBER_PRUNE.
    """

    message_id: Snowflake | None = None
    """ID of the message that was targeted.

    MESSAGE_PIN & MESSAGE_UNPIN.
    """

    role_name: str | None = None
    """Name of the role if type is '0' (not present if type is '1').
    CHANNEL_OVERWRITE_CREATE & CHANNEL_OVERWRITE_UPDATE & CHANNEL_OVERWRITE_DELETE.
    """

    type: str | None = None
    """Type of overwritten entity - role('0') or member('1').

    CHANNEL_OVERWRITE_CREATE & CHANNEL_OVERWRITE_UPDATE & CHANNEL_OVERWRITE_DELETE.
    """

    integration_type: str | None = None
    """The type of integration which performed the action.

    MEMBER_KICK & MEMBER_ROLE_UPDATE.
        """


class AuditLogEntryOut(BaseModel):
    """Audit log entry object.

    Reference:
    https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-audit-log-entry-structure
    """

    target_id: str | None = None
    """ID of the affected entity(webhook, user, role, etc.)."""

    changes: list[AuditLogChangeOut] | None = None
    """Changes made to the target_id."""

    user_id: Snowflake | None = None
    """User or app that made the changes."""

    id: Snowflake | None = None
    """ID of the entry."""

    action_type: FallbackAdapter[AuditLogEvents] | None = None
    """Type of action that occurred."""

    options: OptionalAuditLogEntryInfoOut | None = None
    """Additional info for certain event types."""

    reason: str | None = None
    """Reason for the change (1-512 characters)"""


class AuditLogResponse(BaseModel):
    """AuditLog object.

    Reference:
    https://discord.com/developers/docs/resources/audit-log#audit-log-object-audit-log-structure
    """

    application_commands: list[ApplicationCommandResponse] | None = None
    """List of application commands referenced in the audit log."""

    audit_log_entries: list[AuditLogEntryOut] | None = None
    """List of audit log entries, sorted from most to least recent."""

    auto_moderation_rules: list[AutoModerationRule] | None = None
    """List of auto moderation rules referenced in the audit log."""

    guild_scheduled_events: list[ScheduledEventResponse] | None = None
    """List of guild scheduled events referenced in the audit log."""

    integrations: list[AuditLogIntegrationOut] | None = None
    """List of partial integration objects."""

    threads: list[ThreadResponse] | None = None
    """List of threads referenced in the audit log."""

    users: list[UserResponse] | None = None
    """List of users referenced in the audit log."""

    webhooks: list[WebhookResponse] | None = None
    """List of webhooks referenced in the audit log."""


class WidgetSettingsResponse(BaseModel):
    """Widget settings object.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-widget-settings-object
    """

    enabled: bool
    """Whether the widget is enabled."""

    channel_id: Snowflake | None
    """Widget channel id."""


class WidgetUserResponse(BaseModel):
    """Partial user object for Widget object.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-widget-object-example-guild-widget
    """

    id: Snowflake
    """Id of the user. Anonymized!"""

    username: str
    """Username of the user."""

    discriminator: str
    """Discriminator of the user. Anonymized!"""

    avatar: str | None
    """Avatar hash of the user. Anonymized!"""

    status: str
    """Status of the user."""

    avatar_url: str
    """Avatar url of the user."""


class WidgetChannelResponse(BaseModel):
    """Partial channel object for Widget response.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-widget-object-example-guild-widget
    """

    id: Snowflake
    """Channel id."""

    name: str
    """Channel name."""

    position: int
    """Channel position."""


class WidgetResponse(BaseModel):
    """Widget object.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-widget-object
    """

    id: Snowflake
    """Guild id."""

    name: str
    """Guild name."""

    instant_invite: str | None
    """Instant Invite for the guilds cpecified widget invite channel."""

    channels: list[WidgetChannelResponse]
    """Voice and stage channels which are accessible by everyone."""

    members: list[WidgetUserResponse]
    """Special Widget user objects that includes users presense."""

    presence_count: int
    """Number of online members in this guid."""


class VanityUrlInviteResponse(BaseModel):
    """Vanity URL invite object.

    Reference:
    https://discord.com/developers/docs/resources/guild#get-guild-vanity-url-example-partial-invite-object
    """

    code: str
    """Vanity URL code."""

    uses: int
    """Number of times this invite has been used."""


class OnboardingPromptOptionOut(BaseModel):
    """Onboarding Prompt Option object.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-onboarding-object-prompt-option-structure
    """

    id: Snowflake
    """Id of the prompt option."""

    channel_ids: list[Snowflake]
    """Id for channels a member is added to when the option is selected."""

    role_ids: list[Snowflake]
    """Id for roles assigned to a member when the option is selected."""

    emoji: EmojiResponse | None = None
    """Emoji of the option."""

    title: str
    """Title of the option."""

    description: str | None = None
    """Description of the option."""


class OnboardingPromptOut(BaseModel):
    """Onboarding Prompt object.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-onboarding-object-onboarding-prompt-structure
    """

    id: Snowflake
    """ID of the prompt."""
    type: FallbackAdapter[OnboardingPromptType]
    """Type of prompt."""

    options: list[OnboardingPromptOptionOut]
    """Options available within the prompt."""

    title: str
    """Title of the prompt."""

    single_select: bool
    """Indicates whether users are limited to selecting one option for the prompt."""

    required: bool
    """Indicates whether the prompt is required.

    Before a user completes the onboarding flow.
    """

    in_onboarding: bool
    """Indicates whether the prompt is present in the onboarding flow.

    If false, the prompt will only appear in the Channels & Roles tab.
    """


class OnboardingResponse(BaseModel):
    """Onboarding object.

    Reference:
    https://discord.com/developers/docs/resources/guild#guild-onboarding-object-guild-onboarding-structure
    """

    guild_id: Snowflake
    """ID of the guild this onboarding is part of."""

    prompts: list[OnboardingPromptOut]
    """Prompts shown during onboarding and in customize community."""

    default_channel_ids: list[Snowflake]
    """Channel IDs that members get opted into automatically."""

    enabled: bool
    """Whether onboarding is enabled in the guild."""

    mode: FallbackAdapter[OnboardingMode]
    """Current mode of onboarding."""
