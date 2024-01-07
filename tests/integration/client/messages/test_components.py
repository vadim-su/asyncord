import re

import pytest

from asyncord.client.messages.models.requests.components import (
    ActionRowIn,
    ButtonIn,
    ButtonStyle,
    ComponentType,
    SelectMenuIn,
    SelectMenuOptionIn,
)
from asyncord.client.messages.models.requests.messages import CreateMessageRequest
from asyncord.client.messages.resources import MessageResource


async def test_create_message_with_buttons(messages_res: MessageResource):
    components = [
        ActionRowIn(
            components=[
                ButtonIn(
                    label='Primary',
                    style=ButtonStyle.PRIMARY,
                    custom_id='primary',
                ),
                ButtonIn(
                    label='Secondary',
                    style=ButtonStyle.SECONDARY,
                    custom_id='secondary',
                ),
                ButtonIn(
                    label='Success',
                    style=ButtonStyle.SUCCESS,
                    custom_id='success',
                ),
                ButtonIn(
                    label='Danger',
                    style=ButtonStyle.DANGER,
                    custom_id='danger',
                ),
                ButtonIn(
                    label='Link',
                    style=ButtonStyle.LINK,
                    url='https://discord.com',
                ),  # type: ignore
            ],
        ),
    ]
    message = await messages_res.create(
        CreateMessageRequest(
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
        CreateMessageRequest(components=[component])


def test_dont_create_message_with_button_and_select_menu():
    exc_text = 'ActionRow containing a select menu cannot also contain buttons'
    with pytest.raises(ValueError, match=exc_text):
        ActionRowIn(
            components=[
                ButtonIn(custom_id='custom_id'),
                SelectMenuIn(
                    custom_id='custom',
                    options=[SelectMenuOptionIn(label='Option 1', value='option_1')],
                ),
            ],
        )
