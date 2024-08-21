"""This module defines the `ComponentEmoji` class, which represents an emoji on a button.

References:
    https://discord.com/developers/docs/interactions/message-components#buttons
"""

from typing import Self

from pydantic import BaseModel, model_validator

from asyncord.snowflake import SnowflakeInputType


class ComponentEmoji(BaseModel):
    """Emoji to be displayed on the button.

    At least one of `name` or `id` must be provided, and it can be only one of them.
    Name is used for unicode emojis,
    Id is a snowflake of custom emojis.

    Reference:
        https://discord.com/developers/docs/interactions/message-components#buttons
    """

    name: str | None = None
    """Name of the emoji."""

    id: SnowflakeInputType | None = None
    """ID of the emoji."""

    animated: bool | None = None
    """Whether the emoji is animated."""

    @model_validator(mode='after')
    def name_or_id_required(self) -> Self:
        """Check that `name` or `id` is set."""
        if not self.name and not self.id:
            raise ValueError('At least one of `name` or `id` must be provided')

        if self.name and self.id:
            raise ValueError('Only one of `name` or `id` must be provided')

        return self
