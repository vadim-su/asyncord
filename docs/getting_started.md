# 📖 Getting Started

## First Things First
If you have any questions or need help,
feel free to ask in our [:simple-discord: Discord server](https://discord.gg/Fgzpwtwdtm)!

## Quick Start Guide
To get started with Asyncord, first install the library using pip:

```bash
pip install asyncord
```

## Basic Bot Example
Here's a basic example of a bot that responds to a message with a smiley emoji.

```python title="echo_bot.py"
import asyncio


from asyncord.client.messages.models.requests.messages import CreateMessageRequest
from asyncord.client.rest import RestClient # (1)!
from asyncord.client_hub import ClientHub
from asyncord.gateway.events.messages import MessageCreateEvent

API_TOKEN: str = 'YOUR_SECRET_TOKEN'

async def on_message(message: MessageCreateEvent, client: RestClient) -> None:
    """Echoes the message back to the channel."""
    if message.author.bot: # (2)!
        return

    # Prepare the message resource
    message_res = client.channels.messages(message.channel_id)

    # Message sending logic
    await message_res.create(
        CreateMessageRequest(content=message.content + ' :smile:'),
    )

async def main(api_token: str) -> None:
    """Main function to run the bot."""
    async with ClientHub.connect(api_token) as cli_group:
        cli_group.dispatcher.add_handler(on_message) # (3)!

if __name__ == '__main__':
    asyncio.run(main(API_TOKEN))
```
{ .annotate }

1. We prefer explicit imports to avoid namespace pollution

2. Ignore messages from bots.
   Also, it helps to prevent infinite loops to read the bot's own messages

3. Dispatcher detects the event type by the `first argument` and calls the handler with the event object

And that's it! You've created a simple bot that echoes messages back with a smiley emoji. 🎉

Now you can run the bot:

```bash
python echo_bot.py
```
Don't forget to replace `YOUR SECRET TOKEN` with your bot's token.
You can get the token by creating a bot application on the
[Discord Developer Portal](https://discord.com/developers/applications).

## Next Steps

For more examples you can check out the [examples](https://github.com/vadim-su/asyncord/tree/main/examples)
directory in the repository. We already have some examples there:

#### Echo
Is a simple bot that echoes messages back to the channel. Full example of previous code.

#### Gallery
This bot run periodic tasks to archive old forum posts.

#### Levels
This bot tracks user messages and assigns levels based on the number of messages sent.

#### Help Desk
This example shows how to create a help desk bot that assigns tags to users help requests.
