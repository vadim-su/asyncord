from pydantic import BaseModel

from asyncord.client.users.models import User
from asyncord.snowflake import Snowflake


class Emoji(BaseModel):
    """Represents a custom emoji that can be used in messages.

    https://discord.com/developers/docs/resources/emoji#emoji-object
    """

    id: Snowflake | None
    """Emoji id."""

    name: str | None
    """Emoji name.

    Can be null only in reaction emoji objects.
    """

    roles: list[Snowflake] | None = None
    """Roles allowed to use this emoji."""

    user: User | None = None
    """User that created this emoji."""

    require_colons: bool | None = None
    """Whether this emoji must be wrapped in colons."""

    managed: bool | None = None
    """Whether this emoji is managed."""

    animated: bool | None = None
    """Whether this emoji is animated."""

    available: bool | None = None
    """Whether this emoji can be used.
    
    May be false due to loss of Server Boosts.
    """
