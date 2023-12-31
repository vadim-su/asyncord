"""Module containing models for guilds and guild related objects like invites.

Invite models are integrated to this module temporarily until they are moved to
their own module.

Reference:
https://discord.com/developers/docs/resources/guild
"""

from __future__ import annotations

import datetime
import enum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field

from asyncord.base64_image import Base64ImageInput
from asyncord.client.models.channel_data import ChannelType
from asyncord.client.models.emoji import Emoji
from asyncord.client.models.roles import Role
from asyncord.client.models.scheduled_events import ScheduledEvent
from asyncord.client.models.stickers import Sticker
from asyncord.client.models.users import User
from asyncord.snowflake import Snowflake


class CreateGuildChannel(BaseModel):
    """Data for creating a guild channel in a moment of creating guild.

    Reference:
https://discord.com/developers/docs/resources/guild#create-guild-example-partial-channel-object    """

    id: int | None = None
    """Channel ID.
    
    This id is used for parent_id field when creating a category channel
    """

    name: str = Field(min_length=1, max_length=100)
    """channel name.

    1-100 characters.
    """

    type: ChannelType
    """Type of the channel."""

    parent_id: int | None = None
    """Sub category channels are linked to category channel"""


class CreateGuildData(BaseModel):
    """Data for creating a guild.

    Endpoint for which this model is used can only be used by bots
    in less than 10 guilds

    Reference: 
    https://discord.com/developers/docs/resources/guild#create-guild
    """
    name: str = Field(min_length=2, max_length=100)
    """Name of the guild (2-100 characters)."""

    icon: Base64ImageInput | None = None
    """Base64 128x128 image for the guild icon."""

    verification_level: int | None = None
    """Verification level."""

    default_message_notifications: int | None = None
    """Default message notification level."""

    explicit_content_filter: int | None = None
    """Explicit content filter level."""

    roles: list[Role] | None = None
    """New guild roles.

    The first member of the array is used to change properties of the guild's
    @everyone role. If you are trying to bootstrap a guild with additional
    roles, keep this in mind.
    The required id field within each role object is an integer placeholder,
    and will be replaced by the API upon consumption. Its purpose is to allow
    youto overwrite a role's permissions in a channel when also passing in
    channels with the channels array.
    """

    channels: list[CreateGuildChannel] | None = None
    """New guild's channels.

    When using the channels, the position field is ignored, and
    none of the default channels are created.

    The id field within each channel object may be set to an integer
    placeholder, and will be replaced by the API upon consumption.
    Its purpose is to allow you to create `GUILD_CATEGORY` channels by setting
    the parent_id field on any children to the category's id field.

    Category channels must be listed before any children.
    """

    afk_channel_id: Snowflake | None = None
    """ID for afk channel."""

    afk_timeout: int | None = None
    """Afk timeout in seconds."""

    system_channel_id: Snowflake | None = None
    """The id of the channel where guild notices.

    Notices such as welcome messages and boost events are posted.
    """

    system_channel_flags: int | None = None
    """System channel flags."""


class WelcomeScreenChannel(BaseModel):
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


class UpdateWelcomeScreenData(BaseModel):
    """Welcome screen update data.

    Reference: https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen
    """

    enabled: bool | None = None
    """Whether the welcome screen is enabled."""

    welcome_channels: list[WelcomeScreenChannel] | None = Field(None, max_length=5)
    """Channels shown in the welcome screen, max 5."""

    description: str | None = None
    """Server description shown in the welcome screen."""


class WelcomeScreen(BaseModel):
    """Welcome screen object.

    Reference: https://discord.com/developers/docs/resources/guild#welcome-screen-object
    """

    description: str | None
    """Server description shown in the welcome screen."""

    welcome_channels: list[WelcomeScreenChannel] = Field(max_length=5)
    """List of channels shown in the welcome screen.

    Up to 5 channels.
    """


class Guild(BaseModel):
    """Object representing a guild in Discord.

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

    roles: list[Role] | None = None
    """Roles in the guild."""

    emojis: list[Emoji] | None = None
    """Custom guild emojis."""

    features: list[str]
    """Allowed guild features (replaced by str because it often changes without any notifications)."""

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

    welcome_screen: WelcomeScreen | None = None
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


class GuildPreview(BaseModel):
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

    emojis: list[Emoji] | None = None
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


class BeginPruneData(BaseModel):
    """Data for begin prune.

    Reference:
    https://discord.com/developers/docs/resources/guild#begin-guild-prune-json-params
    """

    days: int | None = Field(None, ge=1, le=30)
    """Number of days to count prune for(1 - 30)."""

    compute_prune_count: bool | None = None
    """Whether 'pruned' is returned, discouraged for large guilds."""

    include_roles: list[Snowflake] | None = None
    """Roles to include."""


class Prune(BaseModel):
    """Object returned by the prune endpoints.

    Reference: https://discord.com/developers/docs/resources/guild#get-guild-prune-count
    """

    pruned: int
    """Number of members pruned."""


class VoiceRegion(BaseModel):
    """Object returned by the voice region endpoints.

    Reference: https://discord.com/developers/docs/resources/voice#voice-region-object-voice-region-structure
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


class InviteChannel(BaseModel):
    """Partial channel object in an invite.

    Reference:
    https://discord.com/developers/docs/resources/invite#invite-object-example-invite-object
    """

    id: Snowflake
    """Channel id."""

    name: str
    """Channel name."""

    type: ChannelType
    """Type of channel."""


class InviteGuild(BaseModel):
    """Partial guild object in an invite.

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


class Invite(BaseModel):
    """Object returned by the invite endpoints.

    Reference: https://discord.com/developers/docs/resources/invite#invite-object-invite-structure
    """

    code: str
    """Unique identifier for the invite."""

    guild: InviteGuild | None = None
    """Guild the invite is for."""

    channel: InviteChannel | None
    """channel the invite is for"""

    inviter: User | None = None
    """user who created the invite"""

    target_type: InviteTargetType | None = None
    """Type of target for this voice channel invite."""

    target_user: User | None = None
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

    guild_scheduled_event: ScheduledEvent | None = None
    """Guild scheduled event.

    Return from get_invite endpoint only when `guild_scheduled_event_id` is not None
    and contains a valid id.
    """


@enum.unique
class ExpireBehavior(enum.IntEnum):
    """The behavior of expiring subscribers."""

    REMOVE_ROLE = 0
    """Remove the role."""

    KICK = 1
    """Kick the user."""


class IntegrationAccount(BaseModel):
    """Integration Account Structure.

    Reference: https://discord.com/developers/docs/resources/guild#integration-account-object
    """
    id: str
    """ID of the account."""

    name: str
    """Name of the account."""


class IntegrationApplication(BaseModel):
    """Integration Application Structure.

    Reference: https://discord.com/developers/docs/resources/guild#integration-application-object
    """

    id: Snowflake
    """ID of the app."""

    name: str
    """Name of the app."""

    icon: str | None = None
    """Icon hash of the app"""

    description: str
    """Description of the app."""

    bot: User | None = None
    """Bot associated with this application."""


class GeneralIntegration(BaseModel):
    """Inntegration object for all types of integrations except Dicscord.

    Reference: https://discord.com/developers/docs/resources/guild#integration-object-integration-structure
    """

    id: Snowflake
    """Integration id."""

    name: str
    """Integration name."""

    type: Literal[IntegrationType.TWITCH, IntegrationType.YOUTUBE]
    """Integration type (twitch, youtube, or discord)."""

    enabled: bool
    """Is this integration enabled."""

    syncing: bool
    """Is this integration being synced."""

    role_id: Snowflake
    """ID that this integration uses for "subscribers."""

    enable_emoticons: bool
    """Whether emoticons should be synced for this integration (twitch only currently)."""

    expire_behavior: ExpireBehavior
    """Behavior of expiring subscribers."""

    expire_grace_period: int
    """Grace period (in days) before expiring subscribers."""

    user: User
    """User for this integration."""

    account: IntegrationAccount
    """Integration account information."""

    synced_at: datetime.datetime
    """When this integration was last synced."""

    subscriber_count: int
    """How many subscribers this integration has."""

    revoked: bool
    """Has this integration been revoked."""

    application: IntegrationApplication | None = None
    """Bot or OAuth2 application for discord integrations."""

    scopes: list[str] | None = None
    """Scopes the application has been authorized for."""


class DiscordIntegration(BaseModel):
    """Integration object for Discord integrations.

    Reference:
    https://discord.com/developers/docs/resources/guild#integration-object-integration-structure
    """

    id: Snowflake
    """Integration id."""

    name: str
    """Integration name."""

    type: Literal[IntegrationType.DISCORD]
    """Integration type (twitch, youtube, or discord)."""

    enabled: bool
    """Is this integration enabled"""

    user: User | None = None
    """User for this integration."""

    account: IntegrationAccount
    """Integration account information."""

    application: IntegrationApplication | None = None
    """Bot OAuth2 application for discord integrations."""

    scopes: list[str] | None = None
    """Scopes the application has been authorized for."""


IntegrationVariants = Annotated[GeneralIntegration | DiscordIntegration, Field(discriminator='type')]


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
class MFALevel(enum.IntEnum):
    """Level of Multi Factor Authentication."""

    NONE = 0
    """guild has no MFA/2FA requirement for moderation actions"""

    ELEVATED = 1
    """guild has a 2FA requirement for moderation actions"""


class UnavailableGuild(BaseModel):
    """Unavailable guild object."""

    id: Snowflake
    """Guild ID"""

    unavailable: bool
    """True if this guild is unavailable due to an outage."""
