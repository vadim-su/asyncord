import re

import pytest

from asyncord.client.messages import MessageResource
from asyncord.client.models.messages import CreateMessageData
from asyncord.client.models.components import (
    Button,
    ActionRow,
    TextInput,
    SelectMenu,
    ButtonStyle,
    ComponentType,
    SelectMenuOption,
)


async def test_create_message_with_buttons(messages_res: MessageResource):
    components = [
        ActionRow(
            components=[
                Button(
                    label='Primary',
                    style=ButtonStyle.PRIMARY,
                    custom_id='primary',
                ),
                Button(
                    label='Secondary',
                    style=ButtonStyle.SECONDARY,
                    custom_id='secondary',
                ),
                Button(
                    label='Success',
                    style=ButtonStyle.SUCCESS,
                    custom_id='success',
                ),
                Button(
                    label='Danger',
                    style=ButtonStyle.DANGER,
                    custom_id='danger',
                ),
                Button(
                    label='Link',
                    style=ButtonStyle.LINK,
                    url='https://discord.com',
                ),
            ],
        ),
    ]
    message = await messages_res.create(
        CreateMessageData(
            content='Test message with buttons',
            components=components,
        ),
    )

    try:
        assert message.content == 'Test message with buttons'
        assert len(message.components) == len(components)
    finally:
        await messages_res.delete(message.id)


@pytest.mark.parametrize('component_type', [
    ComponentType.BUTTON,
    ComponentType.STRING_SELECT,
    ComponentType.USER_SELECT,
    ComponentType.ROLE_SELECT,
    ComponentType.MENTIONABLE_SELECT,
    ComponentType.CHANNEL_SELECT,
])
async def test_crate_message_with_some_top_level_components_not_allowed(
    component_type: ComponentType,
):
    component = {'type': component_type, 'custom_id': 'custom_id'}
    if component_type is ComponentType.STRING_SELECT:
        component['options'] = [
            {'label': 'Option 1', 'value': 'option_1'},
            {'label': 'Option 2', 'value': 'option_2'},
        ]

    exc_pattern = re.compile('.* components must be inside ActionRow')
    with pytest.raises(ValueError, match=exc_pattern):
        CreateMessageData(components=[component])


def test_dont_create_message_with_button_and_select_menu():
    exc_text = 'ActionRow containing a select menu cannot also contain buttons'
    with pytest.raises(ValueError, match=exc_text):
        ActionRow(
            components=[
                Button(custom_id='custom_id'),
                SelectMenu(
                    custom_id='custom_id',
                    options=[SelectMenuOption(label='Option 1', value='option_1')],
                ),
            ],
        ),


async def test_create_message_with_text_input(messages_res: MessageResource):
    components = [
        TextInput(
            type=ComponentType.TEXT_INPUT,
            custom_id='custom_id',
            label='Label',
            placeholder='Placeholder',
        ),
    ],
    message = await messages_res.create(
        CreateMessageData(
            content='Test message with text input',
            components=components,
        ),
    )

    try:
        assert message.content == 'Test message with text input'
        assert len(message.components) == len(components)
    finally:
        await messages_res.delete(message.id)
