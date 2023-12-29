# Asyncord

## Introduction

This library offers a Python, asynchronous interface for the [Discord Bot API](https://discord.com/developers/docs/reference). It's compatible with Python versions **3.12+**.

### Key Features

- **GatewayClient**: Handles the WebSocket connection to Discord. This class is essential for managing real-time events such as messages, user updates, and server changes. Designed with asynchronous programming, it efficiently handles a high volume of events.

- **RestClient**: Manages all HTTP requests to the Discord API. It's responsible for operations like sending messages or managing servers and users, ensuring smooth communication with Discord's API.

## Discord API support

All types and methods of the Discord Bot API **10** are supported.

## Installing

You can install or upgrade ``asyncord`` via

```sh
    $ pip install asyncord --upgrade
```

## Quick Start

The followed example shows how to create a simple bot that responds to user messages.
And has a status of "Playing with asyncord".

```py
import aiohttp

from asyncord.client.models.activity import Activity, ActivityType
from asyncord.client.models.messages import CreateMessageData
from asyncord.client.rest import RestClient
from asyncord.gateway.client import GatewayClient
from asyncord.gateway.commands import PresenceUpdateData
from asyncord.gateway.events.base import ReadyEvent
from asyncord.gateway.events.messages import MessageCreateEvent
from asyncord.gateway.intents import Intent

API_TOKEN = 'YOUR_BOT_TOKEN'
APP_ID = 'YOUR_BOT_APP_ID'

DEFAULT_ACTIVITY = Activity(
    type=ActivityType.GAME,
    name='with asyncord',
)


async def main():
    async with aiohttp.ClientSession() as session:
        gw = GatewayClient(
            API_TOKEN,
            intents=Intent.GUILD_PRESENCES | Intent.GUILD_MESSAGES,
            session=session,
        )
        client = RestClient(API_TOKEN)
        client._http._session = session
        gw.dispatcher.add_argument('client', client)

        async def on_ready(
            ready_event: ReadyEvent,
            gateway: GatewayClient
        ) -> None:
            await gw.update_presence(PresenceUpdateData(
                activities=[DEFAULT_ACTIVITY],
            ))

        async def on_message(
            message_create_event: MessageCreateEvent,
            client: RestClient,
        ) -> None:
            if message_create_event.author.bot:
                return
            await client.channels.messages(message_create_event.channel_id).create(
                CreateMessageData(
                    content='Hello, World!'),
            )

        gw.add_handler(on_ready)
        gw.add_handler(on_message)
        await gw.start()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Features


1. **Fully Asynchronous**: Asyncord is built with asynchronous programming from the ground up. 

2. **Full Discord Bot API Coverage**: The library offers complete coverage of the Discord Bot API, enabling access to all the functionalities that Discord provides for bots. This includes handling messages, managing servers, user interactions, and more.

3. **Complete Pydantic Schema Coverage**: Asyncord incorporates full pydantic schema coverage, ensuring robust data validation and management. 

## Contributing

Contributions of all sizes are welcome.

If you find a bug or have a feature request, please report an issue on GitHub.

## License

