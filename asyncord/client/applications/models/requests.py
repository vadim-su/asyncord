"""This module contains models related to Discord applications."""

from enum import IntEnum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from asyncord.base64_image import Base64ImageInputType
from asyncord.client.applications.models.common import (
    ApplicationFlag,
    ApplicationRoleConnectionMetadataType,
)
from asyncord.client.auth.models import OAuthScope
from asyncord.client.models.permissions import PermissionFlag
from asyncord.locale import LocaleInputType
from asyncord.yarl_url import HttpYarlUrl

__all__ = (
    'ApplicationIntegrationType',
    'ApplicationIntegrationTypeConfig',
    'InstallParams',
    'UpdateApplicationRequest',
    'UpdateApplicationRoleConnectionMetadataRequest',
)

APPLICATION_ALLOWED_TYPES = (
    ApplicationFlag.GATEWAY_PRESENCE_LIMITED
    | ApplicationFlag.GATEWAY_GUILD_MEMBERS_LIMITED
    | ApplicationFlag.GATEWAY_MESSAGE_CONTENT_LIMITED
)

"""Allowed application uodate flags."""


class InstallParams(BaseModel):
    """Application install parameters.

    Reference:
    https://discord.com/developers/docs/resources/application#install-params-object-install-params-structure
    """

    scopes: list[OAuthScope]
    """OAuth2 scopes."""

    permissions: PermissionFlag
    """Bitwise flags representing the permissions your application."""


class ApplicationIntegrationType(IntEnum):
    """Application integration type.

    Reference:
    https://discord.com/developers/docs/resources/application#application-object-application-integration-types
    """

    GUILD_INSTALL = 0
    """App is installable to servers."""

    USER_INSTALL = 1
    """App is installable to users."""


class ApplicationIntegrationTypeConfig(BaseModel):
    """Application integration type configuration object.

    Reference:
    https://discord.com/developers/docs/resources/application#application-object-application-integration-type-configuration-object
    """

    oauth2_install_params: InstallParams | None = None
    """	Install params for each installation context's default in-app authorization link.
    """


class UpdateApplicationRequest(BaseModel):
    """Represents data to update an application.

    Reference:
    https://discord.com/developers/docs/resources/application#edit-current-application-json-params
    """

    custom_install_url: str | None = None
    """Default custom authorization URL for the app, if enabled."""

    description: str | None = None
    """Description of the app."""

    role_connections_verification_url: str | None = None
    """Role connection verification URL for the app."""

    install_params: InstallParams | None = None
    """Settings for the app's default in-app authorization link, if enabled."""

    integration_types_config: dict[ApplicationIntegrationType, ApplicationIntegrationTypeConfig] | None = None
    """Default scopes and permissions for each supported installation context.

    Value for each key is an integration type configuration object.
    """

    flags: ApplicationFlag | None = None
    """App's public flags."""

    icon: Base64ImageInputType | None = None
    """Icon for the app."""

    cover_image: Base64ImageInputType | None = None
    """Default rich presence invite cover image for the app."""

    interactions_endpoint_url: HttpYarlUrl | None = None
    """Interactions endpoint URL for the app."""

    tags: (
        Annotated[
            set[Annotated[str, Field(max_length=20)]],
            Field(max_length=5),
        ]
        | None
    ) = None
    """List of tags describing the content and functionality of the app.

    Maximum of 5 tags.
    Maximum of 20 characters per tag.
    """

    @field_validator('flags')
    @classmethod
    def validate_flags(cls, flags: ApplicationFlag | None) -> ApplicationFlag | None:
        """Ensures that the flag is one of the allowed types."""
        if not flags:
            return None

        if (flags & APPLICATION_ALLOWED_TYPES) != flags:
            err_msg = 'Invalid flag. Must be one of the following: ' + ', '.join(
                [
                    'GATEWAY_PRESENCE_LIMITED',
                    'GATEWAY_GUILD_MEMBERS_LIMITED',
                    'GATEWAY_MESSAGE_CONTENT_LIMITED',
                ],
            )
            raise ValueError(err_msg)

        return flags


class UpdateApplicationRoleConnectionMetadataRequest(BaseModel):
    """Application role connection metadata object.

    Reference:
    https://discord.com/developers/docs/resources/application-role-connection-metadata#application-role-connection-metadata-object-application-role-connection-metadata-structure.
    """

    type: ApplicationRoleConnectionMetadataType
    """Type of metadata value."""

    key: Annotated[str, Field(min_length=1, max_length=50, pattern=r'^[a-z0-9_]{1,50}$')]
    """Dictionary key for the metadata field.

    Must be a - z, 0 - 9, or _ characters.
    1 - 50 characters.
    """

    name: Annotated[str, Field(min_length=1, max_length=100)]
    """Name of the metadata field."""

    name_localizations: dict[LocaleInputType, str] | None = None
    """Translations of the name."""

    description: Annotated[str, Field(min_length=1, max_length=200)]
    """Description of the metadata field."""

    description_localizations: dict[LocaleInputType, str] | None = None
    """Translations of the description."""
