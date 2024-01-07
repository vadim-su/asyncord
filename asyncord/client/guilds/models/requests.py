from pydantic import BaseModel, Field

from asyncord.base64_image import Base64ImageInputType
from asyncord.client.channels.models.requests.creation import CreateChannelRequestType
from asyncord.client.guilds.models.common import DefaultMessageNotificationLevel, ExplicitContentFilterLevel
from asyncord.client.roles.models.responses import RoleResponse
from asyncord.snowflake import SnowflakeInputType


class CreateGuildRequest(BaseModel):
    """Data for creating a guild.

    Endpoint for which this model is used can only be used by bots
    in less than 10 guilds

    Reference: 
    https://discord.com/developers/docs/resources/guild#create-guild
    """

    name: str = Field(min_length=2, max_length=100)
    """Name of the guild (2-100 characters)."""

    icon: Base64ImageInputType | None = None
    """Base64 128x128 image for the guild icon."""

    verification_level: int | None = None
    """Verification level."""

    default_message_notifications: DefaultMessageNotificationLevel | None = None
    """Default message notification level."""

    explicit_content_filter: ExplicitContentFilterLevel | None = None
    """Explicit content filter level."""

    roles: list[RoleResponse] | None = None
    """New guild roles.

    The first member of the array is used to change properties of the guild's
    @everyone role. If you are trying to bootstrap a guild with additional
    roles, keep this in mind.
    The required id field within each role object is an integer placeholder,
    and will be replaced by the API upon consumption. Its purpose is to allow
    youto overwrite a role's permissions in a channel when also passing in
    channels with the channels array.
    """

    channels: list[CreateChannelRequestType] | None = None
    """New guild's channels.

    When using the channels, the position field is ignored, and
    none of the default channels are created.

    The id field within each channel object may be set to an integer
    placeholder, and will be replaced by the API upon consumption.
    Its purpose is to allow you to create `GUILD_CATEGORY` channels by setting
    the parent_id field on any children to the category's id field.

    Category channels must be listed before any children.
    """

    afk_channel_id: SnowflakeInputType | None = None
    """ID for afk channel."""

    afk_timeout: int | None = None
    """Afk timeout in seconds."""

    system_channel_id: SnowflakeInputType | None = None
    """The id of the channel where guild notices.

    Notices such as welcome messages and boost events are posted.
    """

    system_channel_flags: int | None = None
    """System channel flags."""


class WelcomeScreenChannelIn(BaseModel):
    """Welcome screen channel object.

    Reference:
    https://discord.com/developers/docs/resources/guild#welcome-screen-object-welcome-screen-channel-structure
    """

    channel_id: SnowflakeInputType
    """ID of the channel."""

    description: str
    """Description of the channel."""

    emoji_id: SnowflakeInputType | None
    """Emoji ID, if the emoji is custom."""

    emoji_name: str | None
    """Emoji name if custom, the unicode character if standard, or null if no emoji is set."""


class UpdateWelcomeScreenRequest(BaseModel):
    """Data for updating a welcome screen.

    Reference: https://discord.com/developers/docs/resources/guild#modify-guild-welcome-screen
    """

    enabled: bool | None = None
    """Whether the welcome screen is enabled."""

    welcome_channels: list[WelcomeScreenChannelIn] | None = Field(None, max_length=5)
    """Channels shown in the welcome screen.
    
    Up to 5 channels can be specified.
    """

    description: str | None = None
    """Server description shown in the welcome screen."""
