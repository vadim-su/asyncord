from __future__ import annotations

import enum

from pydantic import BaseModel

from asyncord.snowflake import Snowflake
from asyncord.client.models.users import UserFlags


class Application(BaseModel):
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

    terms_of_service_url: str | None = None
    """the url of the app's terms of service"""

    privacy_policy_url: str | None = None
    """the url of the app's privacy policy"""

    owner: ApplicationUser | None = None
    """the owner of the application"""

    summary: str | None = None
    """deprecated and will be removed in v11. An empty string"""

    verify_key: str | None = None
    """the hex encoded key for verification in interactions and the `GameSDK's GetTicket`"""

    team: Team | None
    """the app's team"""

    guild_id: Snowflake | None = None
    """the id of the app's guild"""

    primary_sku_id: Snowflake | None = None
    """the id of the app's primary sku"""

    slug: str | None = None
    """the app's slug"""

    cover_image: str | None = None
    """the app's default rich presence invite cover image hash"""

    flags: ApplicationFlag | None = None
    """the application's public flags"""


class ApplicationUser(BaseModel):
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


@enum.unique
class ApplicationFlag(enum.IntFlag):
    """Discord application flag.

    https://discord.com/developers/docs/resources/application#application-object-application-flags
    """

    GATEWAY_PRESENCE = 1 << 12
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    GATEWAY_GUILD_MEMBERS = 1 << 14
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    EMBEDDED = 1 << 17
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    APPLICATION_COMMAND_BADGE = 1 << 23


class Team(BaseModel):
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

    members: list[TeamMember]
    """the members of the team"""


class TeamMember(BaseModel):
    """Represents a Discord team member.

    https://discord.com/developers/docs/topics/teams#data-models-team-member-object
    """

    membership_state: int
    """the membership state of the user on the team"""

    permissions: list[str]
    """the permissions of the team member in the team"""

    team_id: Snowflake
    """the id of the team"""

    user: TeamMemberUser
    """the user that is a member of the team"""


class TeamMemberUser(BaseModel):
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


@enum.unique
class MembershipState(enum.Enum):
    """Discord team member's membership state.

    https://discord.com/developers/docs/topics/teams#data-models-membership-state-enum
    """

    INVITED = 1
    """the user has been invited to the team but has not yet accepted"""

    ACCEPTED = 2
    """the user has accepted the team invite"""


class GuildApplicationCommandPermissions(BaseModel):
    """https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object"""

    id: Snowflake
    """ID of the command or the application ID"""

    application_id: Snowflake
    """ID of the application the command belongs to"""

    guild_id: Snowflake
    """ID of the guild"""

    permissions: list[ApplicationCommandPermissions]
    """Permissions for the command in the guild, max of 100"""


class ApplicationCommandPermissions(BaseModel):
    """https://discord.com/developers/docs/interactions/slash-commands#applicationcommandpermissions"""

    id: Snowflake  # TODO: add permission constants support
    """ID of the command or the application ID.

    It can also be a permission constant (@everyone, @here...)"""

    type: ApplicationCommandPermissionType
    """Type of the permission"""

    permission: bool
    """Allow or deny permission"""


@enum.unique
class ApplicationCommandPermissionType(enum.IntEnum):
    """https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object-application-command-permission-type"""

    ROLE = 1
    """Role permission type"""

    USER = 2
    """User permission type"""

    CHANNEL = 3
    """Channel permission type"""


Application.update_forward_refs()
