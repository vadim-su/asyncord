"""This module contains models related to Discord applications."""

from enum import IntEnum, StrEnum

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from asyncord.base64_image import Base64ImageInputType
from asyncord.client.applications.models.common import (
    ApplicationFlag,
    ApplicationRoleConnectionMetadataType,
)
from asyncord.client.models.permissions import PermissionFlag
from asyncord.locale import LocaleInputType


class OauthScopes(StrEnum):
    """These are a list of all the OAuth2 scopes that Discord supports.

    Some scopes require approval from Discord to use.
    Requesting them from a user without approval from Discord
    may cause errors or undocumented behavior in the OAuth2 flow.

    Reference:
    https://canary.discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes
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


class InstallParams(BaseModel):
    """Application install parameters.

    Reference:
    https://discord.com/developers/docs/resources/application#install-params-object-install-params-structure
    """

    scopes: list[OauthScopes]
    """OAuth2 scopes."""

    permissions: PermissionFlag
    """Bitwise flags representing the permissions your application."""


class ApplicationIntegrationType(IntEnum):
    """Application integration type.

    Reference:
    https://canary.discord.com/developers/docs/resources/application#application-object-application-integration-types
    """

    GUILD_INSTALL = 0
    """App is installable to servers."""

    USER_INSTALL = 1
    """App is installable to users."""


class ApplicationIntegrationTypeConfig(BaseModel):
    """Application integration type configuration object.

    Reference:
    https://canary.discord.com/developers/docs/resources/application#application-object-application-integration-type-configuration-object
    """

    oauth2_install_params: InstallParams | None = None
    """	Install params for each installation context's default in-app authorization link.
    """


class UpdateApplicationRequest(BaseModel):
    """Represents data to update an application.

    Reference:
    https://canary.discord.com/developers/docs/resources/application#edit-current-application-json-params
    """

    custom_install_url: str | None = None
    """Default custom authorization URL for the app, if enabled."""

    description: str | None = None
    """Description of the app."""

    role_connections_verification_url: str | None = None
    """Role connection verification URL for the app."""

    install_params: InstallParams | None = None
    """Settings for the app's default in-app authorization link, if enabled."""

    integration_types_config: (
        dict[
            ApplicationIntegrationType,
            ApplicationIntegrationTypeConfig,
        ]
        | None
    ) = None
    """Default scopes and permissions for each supported installation context.

    Value for each key is an integration type configuration object.
    """

    flags: ApplicationFlag | None = None
    """App's public flags."""

    icon: Base64ImageInputType | None = None
    """Icon for the app."""

    cover_image: Base64ImageInputType | None = None
    """Default rich presence invite cover image for the app."""

    interactions_endpoint_url: str | None = None
    """Interactions endpoint URL for the app."""

    tags: list[str] | None = None
    """List of tags describing the content and functionality of the app.

    Maximum of 5 tags.
    Maximum of 20 characters per tag.
    """

    @field_validator('tags')
    @classmethod
    def validate_tags(
        cls,
        tags: list[str] | None,
        field_info: ValidationInfo,
    ) -> list[str] | None:
        """Ensures that the length of tags is less than or equal to 5.

        And each tag is less than or equal to 20 characters.
        """
        max_tags = 5
        max_tag_length = 20

        if tags is not None:
            if len(tags) > max_tags:
                raise ValueError('Maximum of 5 tags allowed.')
            for tag in tags:
                if len(tag) > max_tag_length:
                    raise ValueError('Maximum of 20 characters per tag allowed.')
        return tags

    @field_validator('flags')
    @classmethod
    def validate_flags(
        cls,
        tags: ApplicationFlag | None,
    ) -> ApplicationFlag:
        """Ensures that the flag is valid."""
        if tags is not None:
            if tags not in {
                ApplicationFlag.GATEWAY_PRESENCE_LIMITED,
                ApplicationFlag.GATEWAY_GUILD_MEMBERS_LIMITED,
                ApplicationFlag.GATEWAY_MESSAGE_CONTENT_LIMITED,
            }:
                raise ValueError('Invalid flag.')
        return tags


class UpdateApplicationRoleConnectionMetadataRequest(BaseModel):
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

    name: str = Field(None, min_length=1, max_length=100)
    """Name of the metadata field.

    (1 - 100 characters).
    """

    name_localizations: dict[LocaleInputType, str] | None = None
    """Translations of the name."""

    description: str = Field(None, min_length=1, max_length=200)
    """Description of the metadata field.

    (1 - 200 characters).
    """
    description_localizations: dict[LocaleInputType, str] | None = None
    """Translations of the description."""

    @field_validator('key')
    @classmethod
    def validate_key(
        cls,
        key: str,
        field_info: ValidationInfo,
    ) -> list[str] | None:
        """Ensures that the length of key is 1 - 50 characters.

        And a - z, 0 - 9, or _ characters.
        """
        max_length = 50
        allowed_symbols = set('abcdefghijklmnopqrstuvwxyz0123456789_')

        if not 1 <= len(key) <= max_length:
            raise ValueError('Key length must be between 1 and 50 characters.')

        if not set(key).issubset(allowed_symbols):
            raise ValueError('Key must contain only a - z, 0 - 9, or _ characters.')

        return key
