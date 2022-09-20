from __future__ import annotations

import enum
from typing import Literal

from pydantic import Field, BaseModel

from asyncord.snowflake import Snowflake
from asyncord.client.models.emoji import Emoji
from asyncord.client.models.roles import Role
from asyncord.client.models.users import User
from asyncord.client.models.channels import Overwrite, ChannelType
from asyncord.client.models.stickers import Sticker


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


class CreateGuildChannel(BaseModel):
    """Data for creating a guild channel.

    https://discord.com/developers/docs/resources/guild#create-guild-channel
    """

    id: Snowflake
    """channel id"""

    name: str = Field(min_length=1, max_length=100)

    type: ChannelType
    """the type of channel"""


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

    roles: Role | None = None
    """roles in the guild"""

    emojis: Emoji | None = None
    """custom guild emojis"""

    features: list[Feature]
    """enabled guild features"""

    mfa_level: int
    """required MFA level for the guild"""

    application_id: Snowflake | None
    """application id of the guild creator if it is bot - created"""

    system_channel_id: Snowflake | None
    """the id of the channel where guild notices such as welcome messages and boost events are posted"""

    system_channel_flags: int
    """system channel flags"""

    rules_channel_id: Snowflake | None
    """the id of the channel where Community guilds can display rules and / or guidelines"""

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
    """approximate number of members in this guild, returned from the GET / guilds / <id > endpoint when with_counts is true"""

    approximate_presence_count: int | None = None
    """approximate number of non - offline members in this guild, returned from the GET / guilds / <id > endpoint when with_counts is true"""

    welcome_screen: WelcomeScreen | None = None
    """the welcome screen of a Community guild, shown to new members, returned in an Invite's guild object"""

    nsfw_level: int
    """guild NSFW level"""

    stickers: Sticker | None = None
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

    features: list[Feature] | None = None
    """enabled guild features"""

    approximate_member_count: int | None = None
    """approximate number of members in this guild"""

    approximate_presence_count: int | None = None
    """approximate number of non - offline members in this guild"""

    description: str | None = None
    """the description for the guild, if the guild is discoverable"""


class Prune(BaseModel):
    """
    Object returned by the prune endpoints.

    Reference: https://discord.com/developers/docs/resources/guild#prune-object
    """
    pruned: int
    """number of members pruned"""


class VoiceRegion(BaseModel):
    """
    Object returned by the voice region endpoints.

    Reference: https://discord.com/developers/docs/resources/voice#voice-region-object-voice-region-structure
    """
    id: Snowflake
    """voice region id"""

    name: str
    """voice region name"""

    optimal: bool
    """whether the voice region is optimal for voice communication"""

    deprecated: bool
    """whether the voice region is deprecated"""

    custom: bool
    """whether the voice region is custom"""


class Invite(BaseModel):
    """
    Object returned by the invite endpoints.

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
    """
    Object returned by the guild create channel endpoints.

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


class InviteChannel(BaseModel):
    """Reference: https://discord.com/developers/docs/resources/invite#invite-object-example-invite-object"""

    id: Snowflake
    """channel id"""

    name: str
    """channel name"""

    type: ChannelType
    """the type of channel"""


@enum.unique
class Feature(str, enum.Enum):
    """
    Guild features.

    Reference: https://discord.com/developers/docs/resources/guild#guild-object-guild-features
    """
    ANIMATED_BANNER = 'ANIMATED_BANNER'
    """guild has access to set an animated guild banner image"""

    ANIMATED_ICON = 'ANIMATED_ICON'
    """guild has access to set an animated guild icon"""

    AUTO_MODERATION = 'AUTO_MODERATION'
    """guild has set up auto moderation rules"""

    BANNER = 'BANNER'
    """guild has access to set a guild banner image"""

    COMMUNITY = 'COMMUNITY'
    """Guild can enable some additional community features.

    Welcome screen, Membership Screening, stage channels and discovery,
    and receives community updates
    """

    DISCOVERABLE = 'DISCOVERABLE'
    """guild is able to be discovered in the directory"""

    FEATURABLE = 'FEATURABLE'
    """guild is able to be featured in the directory"""

    INVITES_DISABLED = 'INVITES_DISABLED'
    """guild has paused invites, preventing new users from joining"""

    INVITE_SPLASH = 'INVITE_SPLASH'
    """guild has access to set an invite splash background"""

    MEMBER_VERIFICATION_GATE_ENABLED = 'MEMBER_VERIFICATION_GATE_ENABLED'
    """guild has enabled Membership Screening"""

    MONETIZATION_ENABLED = 'MONETIZATION_ENABLED'
    """guild has enabled monetization"""

    MORE_STICKERS = 'MORE_STICKERS'
    """guild has increased custom sticker slots"""

    NEWS = 'NEWS'
    """guild has access to create announcement channels"""

    PARTNERED = 'PARTNERED'
    """guild is partnered"""

    PREVIEW_ENABLED = 'PREVIEW_ENABLED'
    """guild can be previewed before joining via Membership Screening or the directory"""

    PRIVATE_THREADS = 'PRIVATE_THREADS'
    """guild has access to create private threads"""

    ROLE_ICONS = 'ROLE_ICONS'
    """guild is able to set role icons"""

    TICKETED_EVENTS_ENABLED = 'TICKETED_EVENTS_ENABLED'
    """guild has enabled ticketed events"""

    VANITY_URL = 'VANITY_URL'
    """guild has access to set a vanity URL"""

    VERIFIED = 'VERIFIED'
    """guild is verified"""

    VIP_REGIONS = 'VIP_REGIONS'
    """guild has access to set 384kbps bitrate in voice"""

    WELCOME_SCREEN_ENABLED = 'WELCOME_SCREEN_ENABLED'
    """guild has enabled the welcome screen"""


class WelcomeScreen(BaseModel):
    """
    Welcome screen object.

    Reference: https://discord.com/developers/docs/resources/guild#welcome-screen-object
    """

    description: str | None
    """The server description shown in the welcome screen"""

    welcome_channels: list[WelcomeScreenChannel] = Field(max_items=5)
    """The channels shown in the welcome screen, up to 5"""


class WelcomeScreenChannel(BaseModel):
    """
    Welcome screen channel object.

    Reference: https://discord.com/developers/docs/resources/guild#welcome-screen-object-welcome-screen-channel-structure
    """

    channel_id: Snowflake
    """The channel's id"""

    description: str
    """The channel's description"""

    emoji_id: Snowflake | None
    """The emoji id, if the emoji is custom"""

    emoji_name: str | None
    """the emoji name if custom, the unicode character if standard, or null if no emoji is set"""


@enum.unique
class DefaultMessageNotificationLevel(enum.IntEnum):
    ALL_MESSAGES = 0
    """Members will receive notifications for all messages by default."""

    ONLY_MENTIONS = 1
    """Members will receive notifications only for messages that @ mention them by default."""


@enum.unique
class MFALevel(enum.IntEnum):
    NONE = 0
    """guild has no MFA/2FA requirement for moderation actions"""

    ELEVATED = 1
    """guild has a 2FA requirement for moderation actions"""


@enum.unique
class InviteTargetType(enum.IntEnum):
    """The target type of an invite."""

    STREAM = 1
    """The invite is for a stream."""


class UnavailableGuild(BaseModel):
    """An unavailable guild object."""

    id: Snowflake
    """guild id"""

    unavailable: bool
    """true if this guild is unavailable due to an outage"""
