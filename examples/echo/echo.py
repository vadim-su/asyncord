"""A simple echo bot that echoes messages back to the channel."""

import asyncio
import os

from dotenv import load_dotenv

from asyncord.client.messages.models.requests.messages import CreateMessageRequest
from asyncord.client.rest import RestClient
from asyncord.client_hub import ClientHub
from asyncord.gateway.events.base import ReadyEvent
from asyncord.gateway.events.messages import MessageCreateEvent

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


async def on_ready(event: ReadyEvent) -> None:  # noqa: RUF029
    """Prints a message when the bot is ready."""
    print(f'{event.user.username} has connected to Discord!')  # noqa: T201


async def on_message(message: MessageCreateEvent, client: RestClient) -> None:
    """Echoes the message back to the channel."""
    if message.author.bot:
        # Ignore messages from bots
        # Also, it helps to prevent infinite loops to read the bot's own messages
        return

    # Prepare the message resource
    message_res = client.channels.messages(message.channel_id)

    # Message sending logic
    await message_res.create(
        CreateMessageRequest(
            content=message.content + ' :smile:',
        ),
    )


async def main(api_token: str) -> None:
    """Main function to run the bot."""
    async with ClientHub.connect(api_token) as client:
        # Dispatcher detects the event type by the first argument
        # and calls the handler with the event object
        client.dispatcher.add_handler(on_ready)
        client.dispatcher.add_handler(on_message)


if __name__ == '__main__':
    asyncio.run(main(API_TOKEN))
