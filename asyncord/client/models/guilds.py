from __future__ import annotations

import datetime
import enum
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from asyncord.client.models.channels import ChannelType, Overwrite
from asyncord.client.models.emoji import Emoji
from asyncord.client.models.roles import Role
from asyncord.client.models.stickers import Sticker
from asyncord.client.models.users import User
from asyncord.snowflake import Snowflake


class CreateGuildChannel(BaseModel):
    """Data for creating a guild channel.

    https://discord.com/developers/docs/resources/guild#create-guild-channel
    """

    id: Snowflake
    """channel id"""

    name: str = Field(min_length=1, max_length=100)

    type: ChannelType
    """the type of channel"""


class CreateGuildData(BaseModel):
    """Data for creating a guild.

    https://discord.com/developers/docs/resources/guild#create-guild
    """
    name: str = Field(min_length=2, max_length=100)
    """Name of the guild (2-100 characters)."""

    icon: str | None = None
    """Base64 128x128 image for the guild icon.

    Exmaple:
        data:image/jpeg;base64,{BASE64_ENCODED_JPEG_IMAGE_DATA}
    """

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
    """The channel's id"""

    description: str
    """The channel's description"""

    emoji_id: Snowflake | None
    """The emoji id, if the emoji is custom"""

    emoji_name: str | None
    """the emoji name if custom, the unicode character if standard, or null if no emoji is set"""


class UpdateWelcomeScreenData(BaseModel):
    """Welcome screen update data.

    Reference: https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen
    """
    enabled: bool | None = None
    """Whether the welcome screen is enabled"""

    welcome_channels: list[WelcomeScreenChannel] | None = Field(None, max_items=5)
    """The channels shown in the welcome screen, max 5"""

    description: str | None = None
    """The server description shown in the welcome screen"""


class WelcomeScreen(BaseModel):
    """Welcome screen object.

    Reference: https://discord.com/developers/docs/resources/guild#welcome-screen-object
    """

    description: str | None
    """The server description shown in the welcome screen."""

    welcome_channels: list[WelcomeScreenChannel] = Field(max_items=5)
    """List of channels shown in the welcome screen.

    Up to 5 channels.
    """


class Guild(BaseModel):
    """Guilds in Discord represent an isolated collection of users and channels.

    https://discord.com/developers/docs/resources/guild#guild-object
    """
    id: Snowflake
    """guild id"""

    name: str
    """guild name(2 - 100 characters, excluding trailing and leading whitespace)"""

    icon: str | None = None
    """icon hash"""

    icon_hash: str | None = None
    """icon hash, returned when in the template object"""

    splash: str | None
    """splash hash"""

    discovery_splash: str | None
    """discovery splash hash.

    only present for guilds with the "DISCOVERABLE" feature
    """

    owner: bool | None = None
    """true if the user is the owner of the guild"""

    owner_id: Snowflake
    """id of owner"""

    permissions: str | None = None
    """total permissions for the user in the guild(excludes overwrites)"""

    region: str | None = None
    """voice region id for the guild(deprecated)"""

    afk_channel_id: Snowflake | None = None
    """id of afk channel"""

    afk_timeout: int
    """afk timeout in seconds"""

    widget_enabled: bool | None = None
    """true if the server widget is enabled"""

    widget_channel_id: Snowflake | None = None
    """the channel id that the widget will generate an invite to, or null if set to no invite"""

    verification_level: int
    """verification level required for the guild"""

    default_message_notifications: int
    """default message notifications level"""

    explicit_content_filter: int
    """explicit content filter level"""

    roles: list[Role] | None = None
    """roles in the guild"""

    emojis: list[Emoji] | None = None
    """custom guild emojis"""

    features: list[str]
    """enabled guild features

    Replaced by str because too often changes without any notifications.
    """

    mfa_level: int
    """required MFA level for the guild"""

    application_id: Snowflake | None
    """application id of the guild creator if it is bot - created"""

    system_channel_id: Snowflake | None
    """the id of the channel where guild notices such as welcome messages and boost events are posted"""

    system_channel_flags: int
    """system channel flags"""

    rules_channel_id: Snowflake | None
    """the id of the channel where Community guilds can display rules and/or guidelines"""

    max_presences: int | None = None
    """the maximum number of presences for the guild(null is always returned, apart from the largest of guilds)"""

    max_members: int
    """the maximum number of members for the guild"""

    vanity_url_code: str | None
    """the vanity url code for the guild"""

    description: str | None
    """the description of a guild"""

    banner: str | None
    """banner hash"""

    premium_tier: int
    """premium tier(Server Boost level)"""

    premium_subscription_count: int
    """the number of boosts this guild currently has"""

    preferred_locale: str
    """the preferred locale of a Community guild

    used in server discovery and notices from Discord, and sent in interactions

    defaults to "en-US"
    """

    public_updates_channel_id: Snowflake | None
    """the id of the channel where admins and moderators of Community guilds receive notices from Discord"""

    max_video_channel_users: int
    """the maximum amount of users in a video channel"""

    approximate_member_count: int | None = None
    """approximate number of members in this guild, returned from the GET/guilds/<id > endpoint when with_counts is true"""

    approximate_presence_count: int | None = None
    """approximate number of non - offline members in this guild, returned from the GET/guilds/<id > endpoint when with_counts is true"""

    welcome_screen: WelcomeScreen | None = None
    """the welcome screen of a Community guild, shown to new members, returned in an Invite's guild object"""

    nsfw_level: int
    """guild NSFW level"""

    stickers: list[Sticker] | None = None
    """custom guild stickers"""

    premium_progress_bar_enabled: bool
    """whether the guild has the boost progress bar enabled"""


class GuildPreview(BaseModel):
    """Guild preview object.

    https://discord.com/developers/docs/resources/guild#guild-preview-object
    """

    id: Snowflake
    """guild id"""

    name: str
    """guild name(2 - 100 characters, excluding trailing and leading whitespace)"""

    icon: str | None
    """icon hash"""

    splash: str | None
    """splash hash"""

    discovery_splash: str | None
    """Discovery splash hash.

    Only present for guilds with the "DISCOVERABLE" feature.
    """

    emojis: list[Emoji] | None = None
    """custom guild emojis"""

    features: list[str]
    """enabled guild features

    Replaced by str because too often changes without any notifications.
    """

    approximate_member_count: int | None = None
    """approximate number of members in this guild"""

    approximate_presence_count: int | None = None
    """approximate number of non - offline members in this guild"""

    description: str | None = None
    """the description for the guild, if the guild is discoverable"""


class BeginPruneData(BaseModel):
    """Data for begin prune.

    https://discord.com/developers/docs/resources/guild#begin-guild-prune-query-string-params
    """

    days: int | None = None
    """number of days to count prune for(1 or more)"""

    compute_prune_count: bool | None = None
    """whether 'pruned' is returned, discouraged for large guilds"""

    include_roles: list[Snowflake] | None = None
    """roles to include"""


class Prune(BaseModel):
    """Object returned by the prune endpoints.

    Reference: https://discord.com/developers/docs/resources/guild#prune-object
    """
    pruned: int
    """number of members pruned"""


class VoiceRegion(BaseModel):
    """Object returned by the voice region endpoints.

    Reference: https://discord.com/developers/docs/resources/voice#voice-region-object-voice-region-structure
    """
    id: str
    """voice region id"""

    name: str
    """voice region name"""

    optimal: bool
    """whether the voice region is optimal for voice communication"""

    deprecated: bool
    """whether the voice region is deprecated"""

    custom: bool
    """whether the voice region is custom"""


class InviteChannel(BaseModel):
    """https://discord.com/developers/docs/resources/invite#invite-object-example-invite-object"""

    id: Snowflake
    """channel id"""

    name: str
    """channel name"""

    type: ChannelType
    """the type of channel"""


@enum.unique
class IntegrationType(enum.StrEnum):
    """Type of integration."""
    TWITCH = 'twitch'
    YOUTUBE = 'youtube'
    DISCORD = 'discord'


@enum.unique
class InviteTargetType(enum.IntEnum):
    """The target type of an invite."""

    STREAM = 1
    """The invite is for a stream."""


class Invite(BaseModel):
    """Object returned by the invite endpoints.

    Reference: https://discord.com/developers/docs/resources/invite#invite-object-invite-structure
    """
    code: str
    """Invite code (unique identifier for the invite)."""

    guild: Guild | None
    """Guild the invite is for."""

    channel: InviteChannel | None = None
    """channel the invite is for"""

    inviter: User | None = None
    """user who created the invite"""

    target_type: InviteTargetType | None = None
    """Type of target for this voice channel invite."""

    target_user: User
    """user the invite is for"""

    target_user_id: Snowflake
    """user id the invite is for"""

    target_user_type: str
    """user type the invite is for"""


class GuildCreateChannel(BaseModel):
    """Object returned by the guild create channel endpoints.

    Reference: https://discord.com/developers/docs/resources/guild#create-guild-channel-json-params
    """

    id: int | None = None
    """channel id"""

    type: ChannelType
    """the type of channel"""

    name: str | None = Field(None, min_length=1, max_length=100)
    """channel name (1 - 100 characters)"""

    topic: str | None = Field(None, min_length=0, max_length=1024)
    """The channel topic(0 - 1024 characters)."""

    bitrate: int | None = None
    """The bitrate ( in bits) of the voice channel."""

    user_limit: int | None = None
    """The user limit of the voice channel."""

    rate_limit_per_user: int | None = Field(None, min=0, max=21600)
    """Amount of seconds a user has to wait before sending another message(0 - 21600).

    Bots, as well as users with the permission manage_messages or manage_channel,
    are unaffected. `rate_limit_per_user` also applies to thread creation.
    Users can send one message and create one thread during each
    `rate_limit_per_user` interval.
    """

    permission_overwrites: list[Overwrite] | None = None
    """explicit permission overwrites for members and roles."""

    parent_id: Snowflake | None = None
    """Parent category or channel id.

    For guild channels: id of the parent category for a channel.
    for threads:
        id of the text channel this thread was created.
    Each parent category can contain up to 50 channels.
    """

    nsfw: bool | None = None
    """Whether the channel is nsfw."""

    rtc_region: str | None = None
    """Voice region id for the voice channel, automatic when set to null."""

    video_quality_mode: int | None = None
    """The camera video quality mode of the voice channel, 1 when not present."""

    default_auto_archive_duration: Literal[60, 1440, 4320, 10080] | None = None
    """Default duration ( in minutes) that the clients (not the API) will use
    for newly created threads.

    To automatically archive the thread after recent activity.
    Can be set to: 60, 1440, 4320, 10080.
    """


@enum.unique
class ExpireBehavior(enum.IntEnum):
    """The behavior of expiring subscribers."""
    REMOVE_ROLE = 0
    KICK = 1


class IntegrationAccount(BaseModel):
    """Integration Account Structure.

    Reference: https://discord.com/developers/docs/resources/guild#integration-account-object
    """
    id: str
    """id of the account"""

    name: str
    """name of the account"""


class IntegrationApplication(BaseModel):
    """Integration Application Structure.

    Reference: https://discord.com/developers/docs/resources/guild#integration-application-object
    """
    id: Snowflake
    """id of the app"""

    name: str
    """name of the app"""

    icon: str | None = None
    """icon hash of the app"""

    description: str
    """description of the app"""

    bot: User | None = None
    """bot associated with this application"""


class GeneralIntegration(BaseModel):
    """Inntegration object for all types of integrations except Dicscord.

    Reference: https://discord.com/developers/docs/resources/guild#integration-object-integration-structure
    """
    id: Snowflake
    """integration id"""

    name: str
    """integration name"""

    type: Literal[IntegrationType.TWITCH, IntegrationType.YOUTUBE]
    """integration type (twitch, youtube, or discord)"""

    enabled: bool
    """is this integration enabled"""

    syncing: bool
    """is this integration being synced"""

    role_id: Snowflake
    """id that this integration uses for "subscribers"""

    enable_emoticons: bool
    """whether emoticons should be synced for this integration (twitch only currently)"""

    expire_behavior: ExpireBehavior
    """the behavior of expiring subscribers"""

    expire_grace_period: int
    """the grace period (in days) before expiring subscribers"""

    user: User
    """user for this integration"""

    account: IntegrationAccount
    """integration account information"""

    synced_at: datetime.datetime
    """when this integration was last synced"""

    subscriber_count: int
    """how many subscribers this integration has"""

    revoked: bool
    """has this integration been revoked"""

    application: IntegrationApplication | None = None
    """the bot/OAuth2 application for discord integrations"""

    scopes: list[str] | None = None
    """the scopes the application has been authorized for"""


class DiscordIntegration(BaseModel):
    """Integration object for Discord integrations.

    Reference:
    https://discord.com/developers/docs/resources/guild#integration-object-integration-structure
    """

    id: Snowflake
    """integration id"""

    name: str
    """integration name"""

    type: Literal[IntegrationType.DISCORD]
    """integration type (twitch, youtube, or discord)"""

    account: IntegrationAccount
    """integration account information"""

    application: IntegrationApplication | None = None
    """the bot/OAuth2 application for discord integrations"""

    scopes: list[str] | None = None
    """the scopes the application has been authorized for"""


IntegrationVariants = Annotated[GeneralIntegration | DiscordIntegration, Field(discriminator='type')]


@enum.unique
class DefaultMessageNotificationLevel(enum.IntEnum):
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
    """An unavailable guild object."""

    id: Snowflake
    """guild id"""

    unavailable: bool
    """true if this guild is unavailable due to an outage"""
