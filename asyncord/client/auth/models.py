"""This module contains the models for the authorization information."""

from __future__ import annotations

import datetime
import enum

from pydantic import BaseModel

from asyncord.client.users.models.responses import UserResponse
from asyncord.typedefs import StrFlag

__all__ = (
    'AuthorizationInfoApplication',
    'AuthorizationInfoResponse',
    'OAuthScope',
)


@enum.unique
class OAuthScope(StrFlag):
    """Represents the OAuth2 scopes.

    It defines the OAuth2 scopes that can be used to authenticate a user with Discord.
    Note: Some scopes may not be currently available for apps, or may require special approval from Discord.

    Reference:
    https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes
    """

    ACTIVITIES_READ = 'activities.read'
    """Allows your app to fetch data from a user's "Now Playing/Recently Played" list.

    Not currently available for apps.
    """

    ACTIVITIES_WRITE = 'activities.write'
    """Allows your app to update a user's activity.

    Not currently available for apps (NOT REQUIRED FOR GAMESDK ACTIVITY MANAGER).
    """

    APPLICATIONS_BUILDS_READ = 'applications.builds.read'
    """Allows your app to read build data for a user's applications."""

    APPLICATIONS_BUILDS_UPLOAD = 'applications.builds.upload'
    """Allows your app to upload/update builds for a user's applications.

    Requires Discord approval.
    """

    APPLICATIONS_COMMANDS = 'applications.commands'
    """Allows your app to add commands to a guild.

    Included by default with the bot scope.
    """

    APPLICATIONS_COMMANDS_UPDATE = 'applications.commands.update'
    """Allows your app to update its commands using a Bearer token.

    Client credentials grant only.
    """

    APPLICATIONS_COMMANDS_PERMISSIONS_UPDATE = 'applications.commands.permissions.update'
    """Allows your app to update permissions for its commands in a guild a user has permissions to."""

    APPLICATIONS_ENTITLEMENTS = 'applications.entitlements'
    """Allows your app to read entitlements for a user's applications."""

    APPLICATIONS_STORE_UPDATE = 'applications.store.update'
    """Allows your app to read and update store data (SKUs, store listings, achievements, etc.).

    This is for a user's applications.
    """

    BOT = 'bot'
    """For oauth2 bots, this puts the bot in the user's selected guild by default."""

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
    """This allows you to read messages from all client channels.

    For local rpc server api access.
    Otherwise restricted to channels/guilds your app creates.
    """

    RELATIONSHIPS_READ = 'relationships.read'
    """Allows your app to know a user's friends and implicit relationships.

    Requires Discord approval.
    """

    ROLE_CONNECTIONS_WRITE = 'role_connections.write'
    """Allows your app to update a user's connection and metadata for the app."""

    RPC = 'rpc'
    """This allows you to control a user's local Discord client.

    For local rpc server accessa.
    Requires Discord approval.
    """

    RPC_ACTIVITIES_WRITE = 'rpc.activities.write'
    """This allows you to update a user's activity.

    For local rpc server access.
    Requires Discord approval.
    """

    RPC_NOTIFICATIONS_READ = 'rpc.notifications.read'
    """For local rpc server access, this allows you to receive notifications pushed out to the user.

    Requires Discord approval.
    """

    RPC_VOICE_READ = 'rpc.voice.read'
    """This allows you to read a user's voice settings and listen for voice events.

    For local rpc server access.
    Requires Discord approval.
    """

    RPC_VOICE_WRITE = 'rpc.voice.write'
    """This allows you to update a user's voice settings.

    For local rpc server access.
    Requires Discord approval.
    """

    VOICE = 'voice'
    """Allows your app to connect to voice on user's behalf and see all the voice members.

    Requires Discord approval.
    """

    WEBHOOK_INCOMING = 'webhook.incoming'
    """This generates a webhook that is returned in the oauth token response for authorization code grants."""


class AuthorizationInfoApplication(BaseModel):
    """Represents the application that authorization is for."""

    id: str
    """ID of the application."""

    name: str
    """Name of the application."""

    icon: str | None
    """Icon hash of the application."""

    description: str
    """Description of the application."""

    bot_public: bool
    """When false only app owner can join the app's bot to guilds"""

    bot_require_code_grant: bool
    """When true the app's bot will only join upon completion of the full oauth2 code grant flow."""

    verify_key: str
    """Hex encoded public key for the application's bot."""


class AuthorizationInfoResponse(BaseModel):
    """Represents the authorization information response."""

    application: AuthorizationInfoApplication
    """Application that authorization is for."""

    scopes: OAuthScope
    """Scopes that user has authorized for application."""

    expires: datetime.datetime
    """Authorization code expiration time."""

    user: UserResponse | None = None
    """User who has authorized.

    If the user has authorized with the identify scope.
    """
