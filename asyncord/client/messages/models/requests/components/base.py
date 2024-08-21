"""This module defines the base component class for the application.

References:
    https://discord.com/developers/docs/interactions/message-components#message-components
"""

from typing import Self

from pydantic import BaseModel, model_validator

from asyncord.client.messages.models.common import ComponentType


class BaseComponent(BaseModel):
    """Base component class."""

    type: ComponentType = None  # type: ignore
    """Type of the component.

    None value just helps to avoid a warning about the required field.
    This field must be set in subclasses.
    """

    @model_validator(mode='after')
    def set_type_field_set(self) -> Self:
        """Set `type` field in `model_fields_set`.

        Add `type` to `model_fields_set` to make `dict(exclude_unset)` work properly.
        We don't need to set 'type' field because it's already set in a component subclasses class,
        but we need to send it to Discord excluding another unset fields.
        """
        self.model_fields_set.add('type')
        return self
