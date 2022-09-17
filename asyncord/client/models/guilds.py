from __future__ import annotations

import enum
from typing import Annotated

from pydantic import Field, BaseModel

from asyncord.typedefs import LikeSnowflake
from asyncord.snowflake import Snowflake
from asyncord.client.models.roles import Role
from asyncord.client.models.users import User

# class CreateGuildChannelData(BaseModel):
#     "name": "naming-things-is-hard",
#   "type": 0,
#   "id": 2,
#   "parent_id": 1
#   id	snowflake	the id of this channel
#   type	integer	the type of channel


class CreateGuildData(BaseModel):
    """Data for creating a guild.

    https://discord.com/developers/docs/resources/guild#create-guild
    """
    name: Annotated[str, Field(min_length=2, max_length=100)]
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

    channels: list[PartialChannel] | None = None
    """New guild's channels.

    When using the channels, the position field is ignored, and
    none of the default channels are created.

    The id field within each channel object may be set to an integer
    placeholder, and will be replaced by the API upon consumption.
    Its purpose is to allow you to create `GUILD_CATEGORY` channels by setting
    the parent_id field on any children to the category's id field.

    Category channels must be listed before any children.
    """

    afk_channel_id: LikeSnowflake | None = None
    """ID for afk channel."""

    afk_timeout: int | None = None
    """Afk timeout in seconds."""

    system_channel_id: LikeSnowflake | None = None
    """The id of the channel where guild notices.

    Notices such as welcome messages and boost events are posted.
    """

    system_channel_flags: int | None = None
    """System channel flags."""


class Guild(BaseModel):
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

    role: dict | None = None
    """roles in the guild"""

    emoji: dict | None = None
    """custom guild emojis"""

    feature: dict | None = None
    """strings	enabled guild features"""

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

    welcome_screen: dict | None = None
    """the welcome screen of a Community guild, shown to new members, returned in an Invite's guild object"""

    nsfw_level: int
    """guild NSFW level"""

    stickers: dict | None = None
    """custom guild stickers"""

    premium_progress_bar_enabled: bool
    """whether the guild has the boost progress bar enabled"""


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

    channel: PartialChannel | None = None
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


class PartialUserGuild(BaseModel):
    """A partial user guild object."""

    id: Snowflake
    """guild id"""

    name: str
    """guild name(2 - 100 characters, excluding trailing and leading whitespace)"""

    icon: str | None = None
    """icon hash"""

    owner: bool | None = None
    """true if the user is the owner of the guild"""

    permissions: str | None = None
    """total permissions for the user in the guild(excludes overwrites)"""

    feature: dict | None = None
    """strings	enabled guild features"""


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
