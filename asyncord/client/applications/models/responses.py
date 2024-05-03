"""This module contains models related to Discord applications.

Reference:
https://discord.com/developers/docs/resources/application
"""

from __future__ import annotations

from typing import Any

from fbenum.adapter import FallbackAdapter
from pydantic import AnyHttpUrl, BaseModel, Field

from asyncord.client.applications.models.common import (
    ApplicationCommandPermissionType,
    ApplicationFlag,
    ApplicationRoleConnectionMetadataType,
)
from asyncord.client.models.permissions import PermissionFlag
from asyncord.client.users.models.responses import UserFlags
from asyncord.locale import LocaleInputType
from asyncord.snowflake import Snowflake


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
    """The user's id."""

    username: str
    """The user's username, not unique across the platform."""

    discriminator: str
    """The user's 4 - digit discord-tag."""

    avatar: str | None
    """The user's avatar hash."""

    flags: UserFlags | None
    """The flags on a user's account."""


class TeamMemberUserOut(BaseModel):
    """Represents a Discord team member user.

    It's a subset of the `asyncord.client.models.users.User` model.
    """

    id: Snowflake
    """The user's id."""

    username: str
    """The user's username, not unique across the platform."""

    discriminator: str
    """The user's 4 - digit discord-tag."""

    avatar: str | None
    """The user's avatar hash."""


class TeamMemberOut(BaseModel):
    """Represents a Discord team member.

    https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    membership_state: int
    """the membership state of the user on the team"""

    permissions: list[str]
    """the permissions of the team member in the team"""

    team_id: Snowflake
    """the id of the team"""

    user: TeamMemberUserOut
    """the user that is a member of the team"""


class TeamOut(BaseModel):
    """Represents a Discord team.

    https://discord.com/developers/docs/topics/teams#data-models-team-object
    """

    id: Snowflake
    """the unique id of the team"""

    name: str
    """the name of the team"""

    icon: str | None
    """the icon hash of the team"""

    owner_user_id: Snowflake
    """the id of the current team owner"""

    members: list[TeamMemberOut]
    """the members of the team"""


class ApplicationOut(BaseModel):
    """Represents a Discord application.

    https://discord.com/developers/docs/resources/application#application-object-application-structure
    """

    id: Snowflake
    """the id of the app"""

    name: str
    """the name of the app"""

    icon: str | None
    """the icon hash of the app"""

    description: str
    """the description of the app"""

    rpc_origins: list[str] | None = None
    """rpc origin urls, if rpc is enabled"""

    bot_public: bool
    """when false only app owner can join the app's bot to guilds"""

    bot_require_code_grant: bool
    """when true the app's bot will only join upon completion of the full oauth2 code grant flow"""

    # TODO: add support for partial user object
    # https://discord.com/developers/docs/resources/application#application-object-application-structure
    # Unknown structure for the partial user object
    bot: dict[str, Any] | None
    """Partial user object for the bot user associated with the app"""

    terms_of_service_url: str | None = None
    """the url of the app's terms of service"""

    privacy_policy_url: str | None = None
    """the url of the app's privacy policy"""

    owner: ApplicationUserOut | None = None
    """the owner of the application"""

    verify_key: str | None = None
    """the hex encoded key for verification in interactions and the `GameSDK's GetTicket`"""

    team: TeamOut | None
    """the app's team"""

    guild_id: Snowflake | None = None
    """the id of the app's guild"""

    primary_sku_id: Snowflake | None = None
    """the id of the app's primary sku"""

    slug: str | None = None
    """the app's slug"""

    cover_image: str | None = None
    """the app's default rich presence invite cover image hash"""

    flags: FallbackAdapter[ApplicationFlag] | None = None
    """the application's public flags"""

    approximate_guild_count: int | None = None
    """Approximate count of guilds the app has been added to"""

    redirect_uris: list[AnyHttpUrl] | None = None
    """Array of redirect URIs for the app"""

    interactions_endpoint_url: AnyHttpUrl | None = None
    """Interactions endpoint URL for the app"""

    role_connections_verification_url: AnyHttpUrl | None = None
    """Application's default role connection verification url."""

    tags: list[str] = Field(default_factory=list, max_length=5)
    """Tags describing the content and functionality of the application.

    Maximum of 5 tags.
    """

    install_params: InstallParamsOut | None = None
    """Settings for the application's default in-app authorization link."""

    custom_install_url: AnyHttpUrl | None = None
    """Application's default custom authorization link"""


class ApplicationCommandPermissionOut(BaseModel):
    """Returned when fetching the permissions for a command in a guild.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object-application-command-permissions-structure
    """

    id: Snowflake  # TODO: add permission constants support
    """ID of the command or the application ID.

    It can also be a permission constant (@everyone, @here...)"""

    type: FallbackAdapter[ApplicationCommandPermissionType]
    """Type of the permission"""

    permission: bool
    """Allow or deny permission"""


class GuildApplicationCommandPermissionsOut(BaseModel):
    """Returned when fetching the permissions for an app's command(s) in a guild.

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
