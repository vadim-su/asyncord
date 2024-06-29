from typing import Annotated, Literal, Self

from pydantic import Field, model_validator

from asyncord.client.messages.models.common import ButtonStyle, ComponentType
from asyncord.client.messages.models.requests.components.base import BaseComponent
from asyncord.client.messages.models.requests.components.emoji import ComponentEmoji


class Button(BaseComponent):
    """Buttons are interactive components that render in messages.

    They can be clicked by users, and send an interaction to your app when clicked.

    * Buttons must be sent inside an Action Row
    * An Action Row can contain up to 5 buttons
    * An Action Row containing buttons cannot also contain any select menu components

    Reference:
    https://discord.com/developers/docs/interactions/message-components#buttons
    """

    type: Literal[ComponentType.BUTTON] = ComponentType.BUTTON  # type: ignore
    """Type of the component.

    Only `ComponentType.BUTTON` is allowed.
    """

    style: ButtonStyle = ButtonStyle.PRIMARY
    """Style of the button."""

    label: Annotated[str, Field(max_length=80)] | None = None
    """Text to be displayed on the button.

    Max 80 characters.
    """

    emoji: ComponentEmoji | None = None
    """Emoji to be displayed on the button."""

    custom_id: Annotated[str, Field(max_length=100)] | None = None
    """Developer-defined identifier for the button.

    Max 100 characters.
    """

    url: str | None = None
    """URL for link-style buttons."""

    disabled: bool = False
    """Whether the button is disabled."""

    @model_validator(mode='after')
    def validate_style(self) -> Self:
        """Check that `custom_id` or `url` are set."""
        custom_id = self.custom_id
        url = self.url

        if self.style is ButtonStyle.LINK:
            if custom_id:
                raise ValueError('`custom_id` is not allowed for link-style buttons')
            if not url:
                raise ValueError('`url` is required for link-style buttons')
        else:
            if url:
                raise ValueError('`url` is not allowed for non-link-style buttons')
            if not custom_id:
                raise ValueError('`custom_id` is required for non-link-style buttons.')

        return self
