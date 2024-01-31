<!-- ### Asyncord -->
<!-- THIS LIBRARY IS NOT FOR discord.py 
WE HATE discord.py -->
Documentation for version: v1.0.0

**Asyncord** is a low-level python 3.12+ library for the Discord API. It provides full support of the Discord API and Gateway, offering a strong typing and Pydantic usage. 

Fast and reliable, Asyncord is a solid tool to work with Discord API. 

## Installation

```bash
pip install asyncord
```

## Usage

```python
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
        client._http_client._session = session
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

## Why use Asyncord?
<!-- THIS LIBRARY IS NOT FOR discord.py 
WE HATE discord.py -->
- **Strong API support** - Asyncord is built on top of API and mimics the API structure.
- **Pydantic usage** - Asyncord uses Pydantic v2 for data validation and serialization.
- **Strong typing** - Asyncord uses type hints for all models and dataclasses.
- **Models division** - Asyncord divides models into incoming and outgoing for ease of use.
- **Separation of concerns** - Asyncord separates the API and Gateway into two different clients.
