from __future__ import annotations

from asyncord.client.commands import BaseCommandResource
from asyncord.client.models.commands import (
    AppCommandOptionType,
    ApplicationCommandOption,
    ApplicationCommandOptionChoice,
    ApplicationCommandType,
    CreateApplicationCommandData,
)


async def test_create_command(commands_res: BaseCommandResource):
    command_data = CreateApplicationCommandData(
        type=ApplicationCommandType.CHAT_INPUT,
        name='test-command',
        name_localizations={'en-US': 'test'},
        description='test command description',
        description_localizations={'en-US': 'Test Command Description'},
        options=[
            ApplicationCommandOption(
                type=AppCommandOptionType.STRING,
                name='test-option',
                description='test option description',
            ),
            ApplicationCommandOption(
                type=AppCommandOptionType.INTEGER,
                name='test-option-2',
                description='test option description 2',
                required=True,
            ),
            ApplicationCommandOption(
                type=AppCommandOptionType.STRING,
                name='test-option-3',
                description='test option description 3',
                choices=[
                    ApplicationCommandOptionChoice(
                        name='test-choice-1',
                        value='test-value-1',
                    ),
                    ApplicationCommandOptionChoice(
                        name='test-choice-2',
                        value='test-value-2',
                    )
                ],
            )
        ],
    )

    # check that the first option is a required integer
    assert command_data.options[0].type == AppCommandOptionType.INTEGER

    command = await commands_res.create(command_data)

    assert command.name == 'test-command'
    assert command.description == 'test command description'
    await commands_res.delete(command.id)


async def test_create_subcommand_group(commands_res: BaseCommandResource):
    command_data = CreateApplicationCommandData(
        type=ApplicationCommandType.CHAT_INPUT,
        name='test-command-group',
        description='test command description',
        options=[
            ApplicationCommandOption(
                type=AppCommandOptionType.SUB_COMMAND_GROUP,
                name='test-subcommand-group',
                description='test subcommand group description',
                options=[
                    ApplicationCommandOption(
                        type=AppCommandOptionType.SUB_COMMAND,
                        name='test-subcommand',
                        description='test subcommand description',
                        options=[
                            ApplicationCommandOption(
                                type=AppCommandOptionType.INTEGER,
                                name='test-option',
                                description='test option description',
                                required=True,
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    command = await commands_res.create(command_data)

    assert command.name == 'test-command-group'
    assert command.description == 'test command description'
    # await commands_res.delete(command.id)


async def test_get_command_list(commands_res: BaseCommandResource):
    assert await commands_res.get_list()


async def test_get_command(commands_res: BaseCommandResource):
    commands_list = await commands_res.get_list()
    command = await commands_res.get(commands_list[0].id)

    assert commands_list[0].id == command.id
    assert commands_list[0].name == command.name
    assert commands_list[0].description == command.description


async def test_convert_command_to_create_command(commands_res: BaseCommandResource):
    commands_list = await commands_res.get_list()
    command = await commands_res.get(commands_list[0].id)

    command_data = CreateApplicationCommandData.from_command(command)
    assert command_data.name == command.name
    assert command_data.description == command.description
    assert command_data.type == command.type
    assert command_data.options == command.options
