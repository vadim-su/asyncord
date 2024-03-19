"""Module containing response models for bans."""

from pydantic import BaseModel

from asyncord.client.users.models.responses import UserResponse


class BanResponse(BaseModel):
    """Ban object.

    Reference:
    https://discord.com/developers/docs/resources/guild#ban-object
    """

    reason: str | None
    """Reason for banning the user."""

    user: UserResponse
    """User that was banned."""
