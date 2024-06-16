"""Models for role requests."""

from pydantic import BaseModel

from asyncord.base64_image import Base64ImageInputType
from asyncord.color import DEFAULT_COLOR, ColorInput
from asyncord.snowflake import SnowflakeInputType

__all__ = (
    'CreateRoleRequest',
    'RolePositionRequest',
    'UpdateRoleRequest',
)


class CreateRoleRequest(BaseModel):
    """Data for creating a role."""

    name: str
    """Name of the role."""

    permissions: str | None = None
    """Bitwise value of the enabled/disabled permissions.

    Defaults to @everyone permissions in guild
    """

    color: ColorInput = DEFAULT_COLOR
    """RGB color value of the role.

    Defaults to 0.
    """

    hoist: bool = False
    """Whether the role should be displayed separately in the sidebar. Defaults to False."""

    icon: Base64ImageInputType | None = None
    """Role's icon image (if the guild has the ROLE_ICONS feature)."""

    unicode_emoji: str | None = None
    """Role's unicode emoji as a standard emoji (if the guild has the ROLE_ICONS feature)."""

    mentionable: bool = False
    """Whether the role should be mentionable.

    Defaults to False.
    """


class RolePositionRequest(BaseModel):
    """Data for changing the position of a role."""

    id: SnowflakeInputType
    """Role id."""

    position: int | None = None
    """Sorting position of the role."""


class UpdateRoleRequest(BaseModel):
    """Data for updating a role."""

    name: str | None = None
    """Name of the role."""

    permissions: str | None = None
    """Bitwise value of the enabled/disabled permissions.

    Defaults to @everyone permissions in guild.
    """

    color: ColorInput | None = None
    """RGB color value of the role."""

    hoist: bool | None = None
    """Whether the role should be displayed separately in the sidebar.

    Defaults to False.
    """

    icon: str | None = None
    """Role's icon image.

    If the guild has the ROLE_ICONS feature.
    Defaults to False.
    """

    unicode_emoji: str | None = None
    """Role's unicode emoji as a standard emoji.

    If the guild has the ROLE_ICONS feature.
    Defaults to False.
    """
    mentionable: bool | None = None
    """Whether the role should be mentionable. Defaults to False."""
