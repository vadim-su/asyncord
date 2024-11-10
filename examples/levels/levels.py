"""A simple bot to count user messages and assign levels to them."""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from asyncord.client.commands.models.requests import CreateApplicationCommandRequest
from asyncord.client.interactions.models.requests import InteractionRespMessageRequest
from asyncord.client.messages.models.requests.embeds import Embed
from asyncord.client.messages.models.requests.messages import CreateMessageRequest
from asyncord.client.rest import RestClient
from asyncord.client_hub import ClientHub
from asyncord.gateway.events.base import ReadyEvent
from asyncord.gateway.events.interactions import ApplicationCommandInteraction, InteractionCreateEvent
from asyncord.gateway.events.messages import MessageCreateEvent

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')


STORAGE: dict[str, UserXP] = {}
"""A dictionary to store the user's XP and level.

The key is the user's ID and the value is the UserXP object.
"""


class UserXP:
    """A class to represent the user's XP and level."""

    def __init__(self, user_id: str) -> None:
        """Initialize the user's XP and level."""
        self.user_id = user_id
        self.xp = 0

        self.level = 0

    def add_xp(self) -> None:
        """Add the given XP to the user's XP."""
        self.xp += 1
        self.level = self.xp // 5  # 5 messages per level

    def get_xp_to_next_level(self) -> int:
        """Get the remaining XP to the next level."""
        return 5 - self.xp % 5

    def is_new_level(self) -> bool:
        """Check if the user has reached a new level."""
        return not (self.xp % 5)


async def register_command(client: RestClient) -> None:
    """Register the command for the bot."""
    command_res = client.applications.commands(APPLICATION_ID)  # type: ignore

    commands = await command_res.get_list()
    for command in commands:
        # Check if the command already exists
        if command.name == 'level':
            return

    command_data = CreateApplicationCommandRequest(
        name='level',
        description='Check your current level.',
    )

    await command_res.create(command_data)


async def on_ready(event: ReadyEvent, client: RestClient) -> None:
    """Prints a message when the bot is ready."""
    await register_command(client)
    print(f'{event.user.username} has connected to Discord!')  # noqa: T201


async def on_message(message: MessageCreateEvent, client: RestClient) -> None:
    """Count the user's messages and assign levels."""
    if message.author.bot:
        # Ignore messages from bots
        return

    user_id = str(message.author.id)
    if user_id not in STORAGE:
        STORAGE[user_id] = UserXP(user_id)

    user_xp = STORAGE[user_id]
    user_xp.add_xp()

    if not user_xp.is_new_level():
        return

    # Prepare the message resource
    message_res = client.channels.messages(message.channel_id)

    # Message sending logic
    await message_res.create(
        make_congrads_message(user_xp),
    )


async def on_get_level(interaction: InteractionCreateEvent, client: RestClient) -> None:
    """Get the user's current level."""
    if type(interaction.root) is not ApplicationCommandInteraction:
        return

    app_interaction = interaction.root

    if not app_interaction.member or not app_interaction.member.user:
        raise ValueError('Member not found in the interaction.')

    user_id = str(app_interaction.member.user.id)
    if user_id not in STORAGE:
        STORAGE[user_id] = UserXP(user_id)

    user_xp = STORAGE[user_id]

    message = make_status_message(user_xp)
    await client.interactions.send_response(
        app_interaction.id,
        app_interaction.token,
        message,
    )


def make_congrads_message(user_xp: UserXP) -> CreateMessageRequest:
    """Make a message to congratulate the user for reaching a new level."""
    embed = Embed(
        title='Level Up!',
        description=(
            f'Congratulations <@{user_xp.user_id}>! You have reached level {user_xp.level}. '
            f'You need {user_xp.get_xp_to_next_level()} more messages to reach the next level.'
        ),
    )

    return CreateMessageRequest(embeds=embed)


def make_status_message(user_xp: UserXP) -> InteractionRespMessageRequest:
    """Make a message to show the user's current level."""
    embed = Embed(
        title='Level Status',
        description=(
            f'You are currently at level {user_xp.level}. '
            f'You need {user_xp.get_xp_to_next_level()} more messages to reach the next level.'
        ),
    )

    return InteractionRespMessageRequest(embeds=embed)


async def main(api_token: str) -> None:
    """Main function to run the bot."""
    async with ClientHub.connect(api_token) as client:
        # Dispatcher detects the event type by the first argument
        # and calls the handler with the event object
        client.dispatcher.add_handler(on_ready)
        client.dispatcher.add_handler(on_message)
        client.dispatcher.add_handler(on_get_level)


if __name__ == '__main__':
    asyncio.run(main(API_TOKEN))  # type: ignore
