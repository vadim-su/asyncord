from __future__ import annotations

import pytest
from asyncord.client.commands import BaseCommandResource
from asyncord.client.models.commands import AppCommandOptionType, ApplicationCommand, ApplicationCommandOptionChoice, ApplicationCommandType, CreateApplicationCommandData, ApplicationCommandOption

from asyncord.client.rest import RestClient
from asyncord.client.http.errors import ClientError

TEST_APP_ID = '934564225769148436'


@pytest.fixture()
async def commands(client: RestClient):
    return client.applications.commands(TEST_APP_ID)


async def test_create_command(commands: BaseCommandResource):
    command_data = CreateApplicationCommandData(
        type=ApplicationCommandType.CHAT_INPUT,
        name='test-command',
        name_localizations={'en-US': 'test'},
        description='test command description',
        description_localizations={'en-US': 'Test Command Description'},
    )
    command = await commands.create(command_data)

    assert command.name == 'test-command'
    assert command.description == 'test command description'
    await commands.delete(command.id)


# TODO: #9 Add test for creating a command with options and choices


async def test_get_command_list(commands: BaseCommandResource):
    assert await commands.get_list()


async def test_get_command(commands: BaseCommandResource):
    commands_list = await commands.get_list()
    command = await commands.get(commands_list[0].id)

    assert commands_list[0].id == command.id
    assert commands_list[0].name == command.name
    assert commands_list[0].description == command.description
