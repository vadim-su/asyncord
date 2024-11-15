
📖 Getting Started
==================

Quick Start Guide
-----------------
To get started with Asyncord, first install the library using pip:

.. code-block:: bash

    pip install asyncord

Basic Bot Example
-----------------
Here's a basic example of a bot that responds to a message with a smiley emoji:

.. code-block:: python

    import asyncio

    # We prefer explicit imports to avoid namespace pollution
    from asyncord.client.messages.models.requests.messages import CreateMessageRequest
    from asyncord.client.rest import RestClient
    from asyncord.client_hub import ClientHub
    from asyncord.gateway.events.messages import MessageCreateEvent

    API_TOKEN: str = 'YOUR_SECRET_TOKEN'


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
            CreateMessageRequest(content=message.content + ' :smile:'),
        )


    async def main(api_token: str) -> None:
        """Main function to run the bot."""
        async with ClientHub.connect(api_token) as client:
            # Dispatcher detects the event type by the first argument
            # and calls the handler with the event object
            client.dispatcher.add_handler(on_message)


    if __name__ == '__main__':
        asyncio.run(main(API_TOKEN))

Configuration
-------------
To configure your bot, you can use environment variables or a configuration file. Here's an example of using environment variables:

.. code-block:: python

    import os
    import asyncord

    bot = asyncord.Bot(command_prefix=os.getenv('COMMAND_PREFIX', '!'))

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    bot.run(os.getenv('BOT_TOKEN'))
