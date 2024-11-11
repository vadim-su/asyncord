"""Example of a bot that sets tag of completion to a message in a forum channel.

When user want to mark a post as solved, they can react with a ✅ emoji.
After that, the bot will set the tag of completion to the message and archive the thread.
"""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from asyncord.client.channels.models.requests.updating import UpdateChannelRequest
from asyncord.client.rest import RestClient
from asyncord.client.threads.models.requests import UpdateThreadRequest
from asyncord.client_hub import ClientHub
from asyncord.gateway.events.base import ReadyEvent
from asyncord.gateway.events.messages import MessageReactionAddEvent

load_dotenv()
API_TOKEN: str = os.getenv('API_TOKEN')  # type: ignore
FORUM_CHANNEL_ID: str = os.getenv('FORUM_CHANNEL_ID')  # type: ignore
FORUM_TAG_ID: str = os.getenv('FORUM_TAG_ID')  # type: ignore


async def on_ready(event: ReadyEvent, client: RestClient) -> None:  # noqa: RUF029
    """Prints a message when the bot is ready."""
    print(f'{event.user.username} has connected to Discord!')  # noqa: T201


async def on_reaction(event: MessageReactionAddEvent, client: RestClient) -> None:
    """Count the user's messages and assign levels."""
    # Event has a thread_id, so we need to check if it's a thread is a child of our forum channel
    thread = await client.channels.threads(channel_id=FORUM_CHANNEL_ID).get(event.channel_id)

    if not thread:
        return

    if event.emoji.name != '✅':
        return

    await client.channels.update(
        event.channel_id,
        channel_data=UpdateChannelRequest(
            applied_tags=[FORUM_TAG_ID],  # type: ignore
        ),
    )

    await client.channels.threads(channel_id=FORUM_CHANNEL_ID).update(
        event.channel_id,
        thread_data=UpdateThreadRequest(
            name=f'[SOLEVED] {thread.name}',
            archived=True,
        ),
    )


async def main(api_token: str) -> None:
    """Main function to run the bot."""
    async with ClientHub.connect(api_token) as client:
        # Dispatcher detects the event type by the first argument
        # and calls the handler with the event object
        client.dispatcher.add_handler(on_ready)
        client.dispatcher.add_handler(on_reaction)


if __name__ == '__main__':
    asyncio.run(main(API_TOKEN))  # type: ignore
