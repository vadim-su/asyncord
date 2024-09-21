"""This module defines the `TextInput` class, which represents a text input component.

References:
    https://discord.com/developers/docs/interactions/message-components#text-inputs
"""

from typing import Annotated, Literal, Self

from pydantic import Field, ValidationInfo, field_validator, model_validator

from asyncord.client.messages.models.common import ComponentType, TextInputStyle
from asyncord.client.messages.models.requests.components.base import BaseComponent


class TextInput(BaseComponent):
    """Text inputs are an interactive component that render on modals.

    They can be used to collect short-form or long-form text.
    Can be used in modal interactions only.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#text-input-object-text-input-structure
    """

    type: Literal[ComponentType.TEXT_INPUT] = ComponentType.TEXT_INPUT  # type: ignore
    """Type of the component.

    Only `ComponentType.TEXT_INPUT` is allowed.
    """

    custom_id: str
    """Developer-defined identifier for the text input.

    Max 100 characters.
    """

    style: TextInputStyle = TextInputStyle.SHORT
    """Style of the text input."""

    label: str = Field(max_length=45)
    """Label of the component.

    Max 45 characters.
    """

    min_length: Annotated[int, Field(ge=0, le=4000)] | None = None
    """Minimum length of the text input.

    Max 4000 characters.
    """

    max_length: Annotated[int, Field(ge=1, le=4000)] | None = None
    """Maximum length of the text input.

    Max 4000 characters.
    """

    required: bool = True
    """Whether the text input is required to be filled."""

    value: Annotated[str, Field(max_length=4000)] | None = None
    """Pre-filled value for this component.

    Max 4000 characters.
    """

    placeholder: Annotated[str, Field(max_length=100)] | None = None
    """Placeholder text.

    Max 100 characters.
    """

    @model_validator(mode='after')
    def set_style_field_set(self) -> Self:
        """Set `style` field in `model_fields_set`.

        Add `style` to `model_fields_set` to make `dict(exclude_unset)` work properly.
        We don't need to set 'style' field because it's already set in a component subclasses class,
        but we need to send it to Discord excluding another unset fields.
        """
        self.model_fields_set.add('style')
        return self

    @field_validator('max_length')
    def validate_length(cls, max_length: int | None, field_info: ValidationInfo) -> int | None:
        """Validate `min_length` and `max_length`."""
        min_length: int | None = field_info.data['min_length']

        if min_length is not None and max_length is not None:
            if min_length > max_length:
                raise ValueError('`min_length` must be less than or equal to `max_length`')

        return max_length
