"""This module contains the request models for the user endpoints."""

from typing import Annotated

from pydantic import BaseModel, Field

from asyncord.base64_image import Base64ImageInputType

__all__ = (
    'UpdateApplicationRoleConnectionRequest',
    'UpdateUserRequest',
)


class UpdateUserRequest(BaseModel):
    """Update current user request model."""

    username: str | None = None
    """Username."""

    avatar: Base64ImageInputType | None = None
    """Avatar image."""

    banner: Base64ImageInputType | None = None
    """Banner image.

    Can be animated gif.
    """


class UpdateApplicationRoleConnectionRequest(BaseModel):
    """Application role connection object.

    Reference:
    https://discord.com/developers/docs/resources/user#update-current-user-application-role-connection-json-params
    """

    platform_name: Annotated[str, Field(max_length=50)] | None = None
    """Vanity name of the platform a bot has connected"""

    platform_username: Annotated[str, Field(max_length=100)] | None = None
    """Username of the platform a bot has connected"""

    metadata: dict[str, str] | None = None
    """Object mapping application role connection metadata keys to their string-ified value.

    For the user on the platform a bot has connected.
    """
