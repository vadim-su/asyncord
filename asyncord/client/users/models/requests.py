"""This module contains the request models for the user endpoints."""

from pydantic import BaseModel

from asyncord.base64_image import Base64ImageInputType


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
