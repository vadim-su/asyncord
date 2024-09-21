"""This module contains models related to Discord applications.

Reference:
https://discord.com/developers/docs/resources/application
"""

from __future__ import annotations

from fbenum.adapter import FallbackAdapter
from pydantic import BaseModel, Field

from asyncord.client.applications.models.common import (
    ApplicationCommandPermissionType,
    ApplicationFlag,
    ApplicationRoleConnectionMetadataType,
)
from asyncord.client.emojis.models.responses import EmojiResponse
from asyncord.client.guilds.models.responses import WelcomeScreenResponse
from asyncord.client.models.permissions import PermissionFlag
from asyncord.client.models.stickers import Sticker
from asyncord.client.roles.models.responses import RoleResponse
from asyncord.client.users.models.responses import PremiumType, UserFlags
from asyncord.color import ColorInput
from asyncord.locale import LocaleInputType
from asyncord.snowflake import Snowflake
from asyncord.yarl_url import HttpYarlUrl

__all__ = (
    'ApplicationCommandPermissionOut',
    'ApplicationOut',
    'ApplicationRoleConnectionMetadataOut',
    'ApplicationUserOut',
    'BotApplicationOut',
    'GuildApplicationCommandPermissionsOut',
    'InstallParamsOut',
    'InviteCreateEventApplication',
    'TeamMemberOut',
    'TeamMemberUserOut',
    'TeamOut',
)


class InstallParamsOut(BaseModel):
    """Application install parameters.

    Reference:
    https://discord.com/developers/docs/resources/application#install-params-object-install-params-structure
    """

    scopes: list[str]
    """OAuth2 scopes.

    Reference:
    https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes
    """

    permissions: PermissionFlag
    """Bitwise flags representing the permissions your application."""


class ApplicationUserOut(BaseModel):
    """Represents a Discord application owner.

    It's a subset of the `asyncord.client.models.users.User` model.
    """

    id: Snowflake
    """User's id."""

    username: str
    """User's username, not unique across the platform."""

    discriminator: str
    """User's 4 - digit discord-tag."""

    avatar: str | None
    """User's avatar hash."""

    flags: UserFlags | None
    """Flags on a user's account."""


class TeamMemberUserOut(BaseModel):
    """Represents a Discord team member user.

    It's a subset of the `asyncord.client.models.users.User` model.

    Reference:
    https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    id: Snowflake
    """User's id."""

    username: str
    """User's username, not unique across the platform."""

    discriminator: str
    """User's 4 - digit discord-tag."""

    avatar: str | None
    """User's avatar hash."""


class TeamMemberOut(BaseModel):
    """Represents a Discord team member.

    Reference:
    https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    membership_state: int
    """Membership state of the user on the team"""

    permissions: list[str]
    """Permissions of the team member in the team"""

    team_id: Snowflake
    """Id of the team"""

    user: TeamMemberUserOut
    """User that is a member of the team"""


class TeamOut(BaseModel):
    """Represents a Discord team.

    Reference:
    https://discord.com/developers/docs/topics/teams#data-models-team-object
    """

    id: Snowflake
    """Unique id of the team"""

    name: str
    """Name of the team"""

    icon: str | None
    """Icon hash of the team"""

    owner_user_id: Snowflake
    """Id of the current team owner"""

    members: list[TeamMemberOut]
    """Members of the team"""


class BotApplicationOut(BaseModel):
    """Partial user object.

    Structure is unclear. A copy of user model with all fields optional.

    Reference:
    https://discord.com/developers/docs/resources/application#application-object-application-structure
    """

    id: Snowflake | None = None
    """User's id."""

    username: str | None = None
    """User's username, not unique across the platform."""

    discriminator: str | None = None
    """User's 4 - digit discord-tag or 0 if the user has no tag."""

    global_name: str | None = None
    """User's global name.

    For bots, this is the application name.
    """

    avatar: str | None = None
    """User's avatar hash."""

    bot: bool | None = None
    """Whether the user belongs to an OAuth2 application."""

    system: bool | None = None
    """Whether the user is an Official Discord System user (part of the urgent message system)"""

    mfa_enabled: bool | None = None
    """Whether the user has two factor enabled on their account."""

    banner: str | None = None
    """User's banner hash."""

    accent_color: ColorInput | None = None
    """User's banner color encoded as an integer representation of hexadecimal color code."""

    locale: str | None = None
    """User's chosen language option."""

    verified: bool | None = None
    """Whether the email on this account has been verified."""

    email: str | None = None
    """User's email."""

    flags: UserFlags | None = None
    """Flags on a user's account."""

    premium_type: PremiumType | None = None
    """Type of Nitro subscription on a user's account."""

    public_flags: UserFlags | None = None
    """Public flags on a user's account."""

    avatar_decoration: str | None = None
    """User's avatar decoration hash.

    Reference:
    https://discord.com/developers/docs/reference#image-formatting
    """


class ApplicationGuildOut(BaseModel):
    """Partial object of the associated guild.

    Structure is unclear. A copy of guild model with all fields optional.

    Reference:
    https://discord.com/developers/docs/resources/application#application-object-application-structure
    """

    id: Snowflake | None = None
    """Guild ID."""

    name: str | None = None
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

    owner_id: Snowflake | None = None
    """ID of owner."""

    permissions: str | None = None
    """Total permissions for the user in the guild (excludes overwrites)."""

    region: str | None = None
    """Voice region ID for the guild (deprecated)."""

    afk_channel_id: Snowflake | None = None
    """ID of AFK channel."""

    afk_timeout: int | None = None
    """AFK timeout in seconds."""

    widget_enabled: bool | None = None
    """True if the server widget is enabled."""

    widget_channel_id: Snowflake | None = None
    """Channel ID that the widget will generate an invite to, or null if set to no invite."""

    verification_level: int | None = None
    """Verification level required for the guild."""

    default_message_notifications: int | None = None
    """Default message notifications level."""

    explicit_content_filter: int | None = None
    """Explicit content filter level."""

    roles: list[RoleResponse] | None = None
    """Roles in the guild."""

    emojis: list[EmojiResponse] | None = None
    """Custom guild emojis."""

    features: list[str] | None = None
    """Allowed guild features.

    Replaced by str because it often changes without any notifications.
    """

    mfa_level: int | None = None
    """Required MFA level for the guild."""

    application_id: Snowflake | None
    """Application ID of the guild creator if it is bot-created."""

    system_channel_id: Snowflake | None
    """ID of the channel where guild notices such as welcome messages and boost events are posted."""

    system_channel_flags: int | None = None
    """System channel flags."""

    rules_channel_id: Snowflake | None
    """ID of the channel where Community guilds can display rules and/or guidelines."""

    max_presences: int | None = None
    """Maximum number of presences for the guild (null is always returned, apart from the largest of guilds)."""

    max_members: int | None = None
    """Maximum number of members for the guild."""

    vanity_url_code: str | None
    """Vanity URL code for the guild."""

    description: str | None
    """Guild description (0-1000 characters)."""

    banner: str | None
    """Guild banner hash."""

    premium_tier: int | None = None
    """Premium tier (Server Boost level)."""

    premium_subscription_count: int | None = None
    """Number of boosts this guild currently has."""

    preferred_locale: str | None = None
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

    nsfw_level: int | None = None
    """Guild NSFW level."""

    stickers: list[Sticker] | None = None
    """custom guild stickers"""

    premium_progress_bar_enabled: bool | None = None
    """Whether the guild has the boost progress bar enabled."""

    safety_alerts_channel_id: Snowflake | None
    """ID of the channel where admins and moderators of Community guilds receive safety alerts from Discord."""


class ApplicationOut(BaseModel):
    """Represents a Discord application.

    Reference:
    https://discord.com/developers/docs/resources/application#application-object-application-structure
    """

    id: Snowflake
    """Id of the app"""

    name: str
    """Name of the app"""

    icon: str | None
    """Icon hash of the app"""

    description: str
    """Description of the app"""

    rpc_origins: list[str] | None = None
    """rpc origin urls, if rpc is enabled"""

    bot_public: bool
    """when false only app owner can join the app's bot to guilds"""

    bot_require_code_grant: bool
    """when true the app's bot will only join upon completion of the full oauth2 code grant flow"""

    bot: BotApplicationOut | None = None
    """Partial user object for the bot user associated with the app"""

    terms_of_service_url: str | None = None
    """Url of the app's terms of service"""

    privacy_policy_url: str | None = None
    """Url of the app's privacy policy"""

    owner: ApplicationUserOut | None = None
    """Owner of the application"""

    verify_key: str | None = None
    """Hex encoded key for verification in interactions and the `GameSDK's GetTicket`"""

    team: TeamOut | None
    """App's team"""

    guild_id: Snowflake | None = None
    """Id of the app's guild"""

    guild: ApplicationGuildOut | None = None
    """Partial object of the associated guild."""

    primary_sku_id: Snowflake | None = None
    """Id of the app's primary sku"""

    slug: str | None = None
    """App's slug"""

    cover_image: str | None = None
    """App's default rich presence invite cover image hash"""

    flags: FallbackAdapter[ApplicationFlag] | None = None
    """Application's public flags"""

    approximate_guild_count: int | None = None
    """Approximate count of guilds the app has been added to"""

    redirect_uris: list[HttpYarlUrl] | None = None
    """Array of redirect URIs for the app"""

    interactions_endpoint_url: HttpYarlUrl | None = None
    """Interactions endpoint URL for the app"""

    role_connections_verification_url: HttpYarlUrl | None = None
    """Application's default role connection verification url."""

    tags: set[str] = Field(default_factory=list, max_length=5)
    """Tags describing the content and functionality of the application.

    Maximum of 5 tags.
    """

    install_params: InstallParamsOut | None = None
    """Settings for the application's default in-app authorization link."""

    custom_install_url: HttpYarlUrl | None = None
    """Application's default custom authorization link"""


class ApplicationCommandPermissionOut(BaseModel):
    """Returned when fetching the permissions for a command in a guild.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object-application-command-permissions-structure
    """

    id: Snowflake
    """ID of the command or the application ID.

    It can also be a permission constant (@everyone, @here...)
    @everyone is Guild ID.
    All Channels is Guild ID - 1.
    """

    type: FallbackAdapter[ApplicationCommandPermissionType]
    """Type of the permission"""

    permission: bool
    """Allow or deny permission"""


class GuildApplicationCommandPermissionsOut(BaseModel):
    """Returned when fetching the permissions for an app's command(s) in a guild.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object
    """

    id: Snowflake
    """ID of the command or the application ID.

    When the id field is the application ID instead of a command ID,
    the permissions apply to all commands that do not contain explicit overwrites.
    """

    application_id: Snowflake
    """ID of the application the command belongs to."""

    guild_id: Snowflake
    """Guild id."""

    permissions: list[ApplicationCommandPermissionOut]
    """Permissions for the command in the guild.

    Maximum of 100.
    """


class ApplicationRoleConnectionMetadataOut(BaseModel):
    """Application role connection metadata object.

    Reference:
    https://discord.com/developers/docs/resources/application-role-connection-metadata#application-role-connection-metadata-object-application-role-connection-metadata-structure.
    """

    type: ApplicationRoleConnectionMetadataType
    """Type of metadata value."""

    key: str
    """Dictionary key for the metadata field.

    Must be a - z, 0 - 9, or _ characters;
    1 - 50 characters.
    """

    name: str
    """Name of the metadata field.

    (1 - 100 characters).
    """

    name_localizations: dict[LocaleInputType, str] | None = None
    """Translations of the name."""

    description: str
    """Description of the metadata field.

    (1 - 200 characters).
    """
    description_localizations: dict[LocaleInputType, str] | None = None
    """Translations of the description."""


class InviteCreateEventApplication(BaseModel):
    """Partial application object.

    Structure is unclear. A copy of application model with all fields optional.

    Reference:
    https://discord.com/developers/docs/topics/gateway-events#invite-create-invite-create-event-fields
    """

    id: Snowflake | None = None
    """Id of the app"""

    name: str | None = None
    """Name of the app"""

    icon: str | None
    """Icon hash of the app"""

    description: str | None = None
    """Description of the app"""

    rpc_origins: list[str] | None = None
    """rpc origin urls, if rpc is enabled"""

    bot_public: bool | None = None
    """when false only app owner can join the app's bot to guilds"""

    bot_require_code_grant: bool | None = None
    """when true the app's bot will only join upon completion of the full oauth2 code grant flow"""

    bot: BotApplicationOut | None = None
    """Partial user object for the bot user associated with the app"""

    terms_of_service_url: str | None = None
    """Url of the app's terms of service"""

    privacy_policy_url: str | None = None
    """Url of the app's privacy policy"""

    owner: ApplicationUserOut | None = None
    """Owner of the application"""

    verify_key: str | None = None
    """Hex encoded key for verification in interactions and the `GameSDK's GetTicket`"""

    team: TeamOut | None
    """App's team"""

    guild: ApplicationGuildOut | None = None
    """Partial object of the associated guild."""

    guild_id: Snowflake | None = None
    """Id of the app's guild"""

    primary_sku_id: Snowflake | None = None
    """Id of the app's primary sku"""

    slug: str | None = None
    """App's slug"""

    cover_image: str | None = None
    """App's default rich presence invite cover image hash"""

    flags: FallbackAdapter[ApplicationFlag] | None = None
    """Application's public flags"""

    approximate_guild_count: int | None = None
    """Approximate count of guilds the app has been added to"""

    redirect_uris: list[HttpYarlUrl] | None = None
    """Array of redirect URIs for the app"""

    interactions_endpoint_url: HttpYarlUrl | None = None
    """Interactions endpoint URL for the app"""

    role_connections_verification_url: HttpYarlUrl | None = None
    """Application's default role connection verification url."""

    tags: list[str] = Field(default_factory=list, max_length=5)
    """Tags describing the content and functionality of the application.

    Maximum of 5 tags.
    """

    install_params: InstallParamsOut | None = None
    """Settings for the application's default in-app authorization link."""

    custom_install_url: HttpYarlUrl | None = None
    """Application's default custom authorization link"""
