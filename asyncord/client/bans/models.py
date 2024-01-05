from pydantic import BaseModel

from asyncord.client.users.models import UserOutput


class BanOutput(BaseModel):
    """Ban object.

    Reference:
    https://discord.com/developers/docs/resources/guild#ban-object
    """
    reason: str | None
    """Reason for banning the user."""

    user: UserOutput
    """User that was banned."""
