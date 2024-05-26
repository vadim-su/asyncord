"""This module contains the common models for the applications resources."""

import enum


@enum.unique
class ApplicationCommandPermissionType(enum.IntEnum):
    """Discord application command permission type.

    Reference:
    https://discord.com/developers/docs/interactions/application-commands#application-command-permissions-object-application-command-permission-type
    """

    ROLE = 1
    """Role permission type"""

    USER = 2
    """User permission type"""

    CHANNEL = 3
    """Channel permission type"""


@enum.unique
class MembershipState(enum.Enum):
    """Discord team member's membership state.

    https://discord.com/developers/docs/topics/teams#data-models-membership-state-enum
    """

    INVITED = 1
    """the user has been invited to the team but has not yet accepted"""

    ACCEPTED = 2
    """the user has accepted the team invite"""


@enum.unique
class ApplicationFlag(enum.IntFlag):
    """Discord application flag.

    https://discord.com/developers/docs/resources/application#application-object-application-flags
    """

    APPLICATION_AUTO_MODERATION_RULE_CREATE_BADGE = 1 << 6
    GATEWAY_PRESENCE = 1 << 12
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    GATEWAY_GUILD_MEMBERS = 1 << 14
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    EMBEDDED = 1 << 17
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    APPLICATION_COMMAND_BADGE = 1 << 23


@enum.unique
class ApplicationRoleConnectionMetadataType(enum.IntEnum):
    """Discord application role connection metadata type.

    Reference:
    https://discord.com/developers/docs/resources/application-role-connection-metadata#application-role-connection-metadata-object-application-role-connection-metadata-type
    """

    INTEGER_LESS_THAN_OR_EQUAL = 1
    """Metadata value(integer) is less than or equal to the guild's configured value.

    (integer).
    """

    INTEGER_GREATER_THAN_OR_EQUAL = 2
    """Metadata value (integer) is greater than or equal

    to the guild's configured value (integer).
    """

    INTEGER_EQUAL = 3
    """Metadata value (integer) is equal

    to the guild's configured value (integer).
    """

    INTEGER_NOT_EQUAL = 4
    """Metadata value (integer) is not equal

    to the guild's configured value (integer).
    """

    DATETIME_LESS_THAN_OR_EQUAL = 5
    """Metadata value (ISO8601 string) is less than or equal

    to the guild's configured value (integer; days before current date).
    """

    DATETIME_GREATER_THAN_OR_EQUAL = 6
    """Metadata value (ISO8601 string) is greater than or equal

    to the guild's configured value (integer; days before current date).
    """

    BOOLEAN_EQUAL = 7
    """Metadata value (integer) is equal

    to the guild's configured value (integer; 1).
    """

    BOOLEAN_NOT_EQUAL = 8
    """Metadata value (integer) is not equal

    to the guild's configured value (integer; 1).
    """


class OauthScopes(enum.StrEnum):
    """These are a list of all the OAuth2 scopes that Discord supports.

    Some scopes require approval from Discord to use.
    Requesting them from a user without approval from Discord
    may cause errors or undocumented behavior in the OAuth2 flow.

    Reference:
    https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes
    """

    ACTIVITIES_READ = 'activities.read'
    """Allows your app to fetch data from a user's list.

    The list is "Now Playing/Recently Played".
    Not currently available for apps.
    """

    ACTIVITIES_WRITE = 'activities.write'
    """Allows your app to update a user's activity.

    Not currently available for apps (NOT REQUIRED FOR GAMESDK ACTIVITY MANAGER).
    """

    APPLICATIONS_BUILDS_READ = 'applications.builds.read'
    """Allows your app to read build data for a user's applications."""

    APP_BUILDS_UPLOAD = 'applications.builds.upload'
    """Allows your app to upload/update builds for a user's applications.

    Requires Discord approval.
    """

    APP_COMMANDS = 'applications.commands'
    """Allows your app to add commands to a guild - included by default with the bot scope."""

    APP_COMMANDS_UPDATE = 'applications.commands.update'
    """Allows your app to update its commands using a Bearer token - client credentials grant only."""

    APP_COMMANDS_PERM_UPDATE = 'applications.commands.permissions.update'
    """Allows your app to update permissions for its commands in a guild a user has permissions to."""

    APP_ENTITLEMENTS = 'applications.entitlements'
    """Allows your app to read entitlements for a user's applications."""

    APP_STORY_UPDATE = 'applications.store.update'
    """Allows your app to read and update store data.

    (SKUs, store listings, achievements, etc.) for a user's applications.
    """

    BOT = 'bot'
    """for oauth2 bots, this puts the bot in the user's selected guild by default."""

    CONNECTIONS = 'connections'
    """Allows /users/@me/connections to return linked third-party accounts."""

    DM_CHANNELS_READ = 'dm_channels.read'
    """Allows your app to see information about the user's DMs and group DMs.

    Requires Discord approval.
    """

    EMAIL = 'email'
    """Enables /users/@me to return an email."""

    GDM_JOIN = 'gdm.join'
    """Allows your app to join users to a group dm."""

    GUILDS = 'guilds'
    """Allows /users/@me/guilds to return basic information about all of a user's guilds."""

    GUILDS_JOIN = 'guilds.join'
    """Allows /guilds/{guild.id}/members/{user.id} to be used for joining users to a guild."""

    GUILDS_MEMBERS_READ = 'guilds.members.read'
    """Allows /users/@me/guilds/{guild.id}/member to return a user's member information in a guild."""

    IDENTIFY = 'identify'
    """Allows /users/@me without email."""

    MESSAGES_READ = 'messages.read'
    """for local rpc server api access, this allows you to read messages from all client channels

    (otherwise restricted to channels/guilds your app creates)."""

    RELATIONSHIPS_READ = 'relationships.read'
    """Allows your app to know a user's friends and implicit relationships.

    Requires Discord approval.
    """

    ROLE_CONNECTIONS_WRITE = 'role_connections.write'
    """Allows your app to update a user's connection and metadata for the app."""

    RPC = 'rpc'
    """for local rpc server access, this allows you to control a user's local Discord client.

    Requires Discord approval.
    """

    RPC_ACTIVITIES_WRITE = 'rpc.activities.write'
    """for local rpc server access, this allows you to update a user's activity.

    Requires Discord approval.
    """

    RPC_NOTIFICATIONS_READ = 'rpc.notifications.read'
    """for local rpc server access, this allows you to receive notifications pushed out to the user.

    Requires Discord approval.
    """

    RPC_VOICE_READ = 'rpc.voice.read'
    """For local rpc server access, this allows you to read a user's voice settings and listen for voice events.

    Requires Discord approval.
    """

    RPC_VOICE_WRITE = 'rpc.voice.write'
    """For local rpc server access, this allows you to update a user's voice settings.

    Requires Discord approval.
    """

    VOICE = 'voice'
    """Allows your app to connect to voice on user's behalf and see all the voice members.

    Requires Discord approval.
    """

    WEBHOOK_INCOMING = 'webhook.incoming'
    """This generates a webhook that is returned in the oauth token response for authorization code grants."""
