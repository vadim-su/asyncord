"""Module containing response models for bans."""

from pydantic import BaseModel

from asyncord.client.users.models.responses import UserResponse
from asyncord.snowflake import SnowflakeInputType

__all__ = (
    'BanResponse',
    'BulkBanResponse',
)


class BanResponse(BaseModel):
    """Ban object.

    Reference:
    https://discord.com/developers/docs/resources/guild#ban-object
    """

    reason: str | None
    """Reason for banning the user."""

    user: UserResponse
    """User that was banned."""


class BulkBanResponse(BaseModel):
    """Bulk ban object.

    Reference:
    https://discord.com/developers/docs/resources/guild#bulk-guild-ban-bulk-ban-response
    """

    banned_users: list[SnowflakeInputType] | None
    """List of user ids, that were successfully banned."""

    failed_users: list[SnowflakeInputType] | None
    """List of user ids, that were not banned."""
