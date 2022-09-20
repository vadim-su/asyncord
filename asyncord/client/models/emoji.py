from pydantic import BaseModel

from asyncord.snowflake import Snowflake
from asyncord.client.models.users import User


class Emoji(BaseModel):
    """Represents a custom emoji that can be used in messages.

    https://discord.com/developers/docs/resources/emoji#emoji-object
    """

    id: Snowflake | None
    """emoji id"""

    name: str | None
    """emoji name

    can be null only in reaction emoji objects
    """

    roles: list[Snowflake] | None = None
    """roles allowed to use this emoji"""

    user: User | None = None
    """the user that created this emoji"""

    require_colons: bool | None = None
    """whether this emoji must be wrapped in colons"""

    managed: bool | None = None
    """whether this emoji is managed"""

    animated: bool | None = None
    """whether this emoji is animated"""

    available: bool | None = None
    """whether this emoji can be used, may be false due to loss of Server Boosts"""
