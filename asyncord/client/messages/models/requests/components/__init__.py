"""This module contains models for the message components.

It's violating agreement that we have in the project to use full names for the module
imports. But current deep nesting of the module is not very readable. So, we decided
to allow import classes directly from the package to decrease the nesting level.
If you want you can use full names for the module imports.
This decision can be changed in the future.

Reference:
https://discord.com/developers/docs/interactions/message-components#message-components
"""

# Action Row
from asyncord.client.messages.models.requests.components.action_row import ActionRow as ActionRow
from asyncord.client.messages.models.requests.components.action_row import MessageComponentType as MessageComponentType

# Base Component
from asyncord.client.messages.models.requests.components.base import BaseComponent as BaseComponent

# Buttons
from asyncord.client.messages.models.requests.components.buttons import ButtonComponentType as ButtonComponentType
from asyncord.client.messages.models.requests.components.buttons import DangerButton as DangerButton
from asyncord.client.messages.models.requests.components.buttons import LinkButton as LinkButton
from asyncord.client.messages.models.requests.components.buttons import PrimaryButton as PrimaryButton
from asyncord.client.messages.models.requests.components.buttons import SecondaryButton as SecondaryButton
from asyncord.client.messages.models.requests.components.buttons import SuccessButton as SuccessButton

# Emoji
from asyncord.client.messages.models.requests.components.emoji import ComponentEmoji as ComponentEmoji

# Selects
from asyncord.client.messages.models.requests.components.selects import SelectDefaultValue as SelectDefaultValue
from asyncord.client.messages.models.requests.components.selects import SelectMenu as SelectMenu
from asyncord.client.messages.models.requests.components.selects import SelectMenuOption as SelectMenuOption
from asyncord.client.messages.models.requests.components.text_input import TextInput as TextInput
