"""This module contains all the necessary components related to OAuth2 authentication for Discord.

Reference: https://discord.com/developers/docs/topics/oauth2
"""

import enum


@enum.unique
class OAuth2Scope(enum.Enum):
    """Represents the OAuth2 scopes.

    It defines the OAuth2 scopes that can be used to authenticate a user with Discord.
    Note: Some scopes may not be currently available for apps, or may require special approval from Discord.

    Reference: https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes
    """

    activities_read = 'activities.read'
    """Allows your app to fetch data from a user's "Now Playing/Recently Played" list.

    Not currently available for apps.
    """

    activities_write = 'activities.write'
    """Allows your app to update a user's activity.

    Not currently available for apps (NOT REQUIRED FOR GAMESDK ACTIVITY MANAGER).
    """

    applications_builds_read = 'applications.builds.read'
    """Allows your app to read build data for a user's applications."""

    applications_builds_upload = 'applications.builds.upload'
    """Allows your app to upload/update builds for a user's applications.

    Requires Discord approval.
    """

    applications_commands = 'applications.commands'
    """Allows your app to add commands to a guild.

    Included by default with the bot scope.
    """

    applications_commands_update = 'applications.commands.update'
    """Allows your app to update its commands using a Bearer token.

    Client credentials grant only.
    """

    applications_commands_permissions_update = 'applications.commands.permissions.update'
    """Allows your app to update permissions for its commands in a guild a user has permissions to."""

    applications_entitlements = 'applications.entitlements'
    """Allows your app to read entitlements for a user's applications."""

    applications_store_update = 'applications.store.update'
    """Allows your app to read and update store data (SKUs, store listings, achievements, etc.).

    This is for a user's applications.
    """

    bot = 'bot'
    """For oauth2 bots, this puts the bot in the user's selected guild by default."""

    connections = 'connections'
    """Allows /users/@me/connections to return linked third-party accounts."""

    dm_channels_read = 'dm_channels.read'
    """Allows your app to see information about the user's DMs and group DMs.

    Requires Discord approval.
    """

    email = 'email'
    """Enables /users/@me to return an email."""

    gdm_join = 'gdm.join'
    """Allows your app to join users to a group dm."""

    guilds = 'guilds'
    """Allows /users/@me/guilds to return basic information about all of a user's guilds."""

    guilds_join = 'guilds.join'
    """Allows /guilds/{guild.id}/members/{user.id} to be used for joining users to a guild."""

    guilds_members_read = 'guilds.members.read'
    """Allows /users/@me/guilds/{guild.id}/member to return a user's member information in a guild."""

    identify = 'identify'
    """Allows /users/@me without email."""

    messages_read = 'messages.read'
    """This allows you to read messages from all client channels.

    For local rpc server api access.
    Otherwise restricted to channels/guilds your app creates.
    """

    relationships_read = 'relationships.read'
    """Allows your app to know a user's friends and implicit relationships.

    Requires Discord approval.
    """

    role_connections_write = 'role_connections.write'
    """Allows your app to update a user's connection and metadata for the app."""

    rpc = 'rpc'
    """This allows you to control a user's local Discord client.

    For local rpc server accessa.
    Requires Discord approval.
    """

    rpc_activities_write = 'rpc.activities.write'
    """This allows you to update a user's activity.

    For local rpc server access.
    Requires Discord approval.
    """

    rpc_notifications_read = 'rpc.notifications.read'
    """For local rpc server access, this allows you to receive notifications pushed out to the user.

    Requires Discord approval.
    """

    rpc_voice_read = 'rpc.voice.read'
    """This allows you to read a user's voice settings and listen for voice events.

    For local rpc server access.
    Requires Discord approval.
    """

    rpc_voice_write = 'rpc.voice.write'
    """This allows you to update a user's voice settings.

    For local rpc server access.
    Requires Discord approval.
    """

    voice = 'voice'
    """Allows your app to connect to voice on user's behalf and see all the voice members.

    Requires Discord approval.
    """

    webhook_incoming = 'webhook.incoming'
    """This generates a webhook that is returned in the oauth token response for authorization code grants."""
