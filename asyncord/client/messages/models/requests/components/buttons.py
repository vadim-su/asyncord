from typing import Annotated, Literal, Self

from pydantic import AnyHttpUrl, Field, model_validator

from asyncord.client.messages.models.common import ButtonStyle, ComponentType
from asyncord.client.messages.models.requests.components.base import BaseComponent
from asyncord.client.messages.models.requests.components.emoji import ComponentEmoji


class BaseButton(BaseComponent):
    """Buttons are interactive components that render in messages.

    They can be clicked by users, and send an interaction to your app when clicked.

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

    disabled: bool = False
    """Whether the button is disabled."""

    @model_validator(mode='after')
    def set_style_field_set(self) -> Self:
        """Set `style` field in `model_fields_set`.

        Add `style` to `model_fields_set` to make `dict(exclude_unset)` work properly.
        We don't need to set 'style' field because it's already set in a component subclasses class,
        but we need to send it to Discord excluding another unset fields.
        """
        self.model_fields_set.add('style')
        return self


class LinkButton(BaseButton):
    """Link-style buttons are interactive components that render in messages.

    They can be clicked by users, and send an interaction to your app when clicked.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#buttons
    """

    style: Literal[ButtonStyle.LINK] = ButtonStyle.LINK  # type: ignore
    """Style of the button.

    Only `ButtonStyle.LINK` is allowed.
    """

    url: Annotated[str, AnyHttpUrl]
    """URL for link-style buttons."""


class AnyButtonWithCustomId(BaseButton):
    """Base class for buttons with a custom ID."""

    style: Literal[  # type: ignore
        ButtonStyle.PRIMARY,
        ButtonStyle.SECONDARY,
        ButtonStyle.SUCCESS,
        ButtonStyle.DANGER,
    ]
    custom_id: Annotated[str, Field(max_length=100)]
    """Developer-defined identifier for the button.

    Max 100 characters.
    """


class PrimaryButton(AnyButtonWithCustomId):
    """Primary-style buttons are interactive components that render in messages.

    They can be clicked by users, and send an interaction to your app when clicked.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#buttons
    """

    style: Literal[ButtonStyle.PRIMARY] = ButtonStyle.PRIMARY  # type: ignore
    """Style of the button.

    Only `ButtonStyle.PRIMARY` is allowed.
    """

    custom_id: Annotated[str, Field(max_length=100)]
    """Developer-defined identifier for the button.

    Max 100 characters.
    """


class SecondaryButton(AnyButtonWithCustomId):
    """Secondary-style buttons are interactive components that render in messages.

    They can be clicked by users, and send an interaction to your app when clicked.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#buttons
    """

    style: Literal[ButtonStyle.SECONDARY] = ButtonStyle.SECONDARY  # type: ignore
    """Style of the button.

    Only `ButtonStyle.SECONDARY` is allowed.
    """

    custom_id: Annotated[str, Field(max_length=100)]
    """Developer-defined identifier for the button.

    Max 100 characters.
    """


class SuccessButton(AnyButtonWithCustomId):
    """Success-style buttons are interactive components that render in messages.

    They can be clicked by users, and send an interaction to your app when clicked.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#buttons
    """

    style: Literal[ButtonStyle.SUCCESS] = ButtonStyle.SUCCESS  # type: ignore
    """Style of the button.

    Only `ButtonStyle.SUCCESS` is allowed.
    """

    custom_id: Annotated[str, Field(max_length=100)]
    """Developer-defined identifier for the button.

    Max 100 characters.
    """


class DangerButton(AnyButtonWithCustomId):
    """Danger-style buttons are interactive components that render in messages.

    They can be clicked by users, and send an interaction to your app when clicked.

    Reference:
    https://discord.com/developers/docs/interactions/message-components#buttons
    """

    style: Literal[ButtonStyle.DANGER] = ButtonStyle.DANGER  # type: ignore
    """Style of the button.

    Only `ButtonStyle.DANGER` is allowed.
    """

    custom_id: Annotated[str, Field(max_length=100)]
    """Developer-defined identifier for the button.

    Max 100 characters.
    """


type ButtonComponentType = Annotated[
    LinkButton | PrimaryButton | SecondaryButton | SuccessButton | DangerButton,
    Field(discriminator='style'),
]
"""Type hint for button components."""
