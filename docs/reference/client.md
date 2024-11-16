# Client

The `ClientHub` class is the main aggregation point for all the client's components.
It provides a way to initialize the group of clients to manage the bot's behavior.
Every group of clients contains:

- `dispatcher` - the event dispatcher to handle discord [events](https://discord.com/developers/docs/events/gateway-events#gateway-events)
- `gateway` - the gateway client to interact with the discord [gateway](https://discord.com/developers/docs/events/gateway#gateway)
- `client` - the rest client to interact with the discord [rest api](https://discord.com/developers/docs/reference#http-api)


## Initialization

### Single bot connection

To initialize the client group, you need to provide your bot's token. We have two ways
to establish a connection for a single bot(1):
{ .annotate }

1. Yeah! You can manage multiple bots in a single script or application.

=== "Using `connect` method"

    ```python
    import asyncio
    from asyncord.client_hub import connect

    API_TOKEN = 'YOUR_SECRET_TOKEN'

    async def main():
        async with connect(API_TOKEN) as cli_group:
            # ...your code to initialize handlers...

    if __name__ == '__main__':
        asyncio.run(main())
    ```

=== "Manual running"

    ```python
    import asyncio
    from asyncord.client_hub import ClientHub

    API_TOKEN = 'YOUR_SECRET_TOKEN'

    async def main():
        client_hub = ClientHub()
        # ...your code to initialize handlers...
        await client_hub.start()
    ```

Also, you can initialize any client separately, like the rest client:(1)
{ .annotate }

1.  It can be useful when you need to make requests outside of the event loop.
    For example, in a web server or a script.

```python
from asyncord.client.rest import RestClient

rest_client = RestClient(API_TOKEN)
response = rest_client.channels.get('channel_id')
print(response.model_dump())
```

### Multiple bot connections

Sometimes you need to manage multiple bots in a single script or application.
You can do this by creating multiple groups of clients:

```python
import asyncio
from asyncord.client_hub import ClientHub

API_TOKEN = 'YOUR_SECRET_TOKEN'

async def main():
    client_hub = ClientHub()
    bot_clients_1 = client_hub.create_client_group('MyBot1', API_TOKEN1)# (1)!
    bot_clients_2 = client_hub.create_client_group('MyBot2' , API_TOKEN2)# (2)!
    ...
    await client_hub.start()
```
{ .annotate }

1. Under the hood, the `connect` method makes the same call to `create_client_group`.
    It is just a shortcut to create a single bot connection.
2. The first argument is the name of the group of clients. It is useful when you need to
    make a call to a specific bot from other groups. For example, you can get an event
    from one bot and send a message from another bot.



## Event Handling

Asyncord follows an event-driven architecture as a way to interact with Discord's API.
The library provides a set of event classes that represent different types of events.

### Event handlers

You can register event handlers
using the `add_handler` method of the client's dispatcher.
Handler functions should accept the event object as the first argument,
and this argument should be annotated. The dispatcher's `add_handler` method
automatically detects the event type from the first argument and invokes
the handler with the event object. If you prefer not to use annotations,
you can specify the event type as the first argument of the `add_handler` method.
The example below illustrates this:

=== "Using annotations"

    ```python
    from asyncord.client_hub import connect
    from asyncord.gateway.events.messages import MessageCreateEvent

    async def on_message(event: MessageCreateEvent, client: RestClient):
        if event.author.bot:
            return
        # ...handle the message event...

    # Register the event handler
    with connect(API_TOKEN) as cli_group:
        cli_group.dispatcher.add_handler(on_message)# (1)!
    ```
    { .annotate }

    1. The dispatcher detects the event type by the first argument of the handler
        and calls the handler with the event object.

=== "Without annotations (not recommended)"

    ```python
    from asyncord.client_hub import connect
    from asyncord.gateway.events.messages import MessageCreateEvent

    async def on_message(event, client):
        if event.author.bot:
            return
        # ...handle the message event...

    # Register the event handler
    with connect(API_TOKEN) as cli_group:
        cli_group.dispatcher.add_handler(MessageCreateEvent, on_message)# (1)!
    ```
    { .annotate }

    1. In this case, you need to specify the event type explicitly as the first
    argument of the `add_handler` method. It is not recommended to use this approach.

    ???+ warning
        The second approach is not recommended because it is less readable and
        can be removed in future versions of the library.

### Handler arguments

The handler function should accept the event object as the first argument.
Other arguments can be added to the dispatcher's `add_argument` method and
will be passed to the handler function by the name of the argument.

For instance, the example below shows how to pass some static number to the handler:

```python
from asyncord.client_hub import connect
from asyncord.gateway.events.messages import MessageCreateEvent

async def on_message(event: MessageCreateEvent, client: RestClient, my_number: int):
    if event.author.bot:
        return
    # ...handle the message event...

# Register the event handler
with connect(API_TOKEN) as cli_group:
    cli_group.dispatcher.add_argument('my_number', 42)# (1)!
    # Now we can use my_number in an event handler 🎉
    cli_group.dispatcher.add_handler(on_message)
```
{ .annotate }

1. The `add_argument` method adds the argument to the pull of arguments that
will be passed to the handler function.

### Default arguments

By default, dispatcher can pass the two default arguments:

- `client` - the rest client instance, to process with rest api of discord
- `gateway` - the gateway instance, to interact and manage different discord
    events using websocket connection
- `client_groups` - the dictionary of all client groups, where the key is the name of the group
    and the value is the group of clients


## How to get main resources?

To access main resources such as guilds, channels, or users, you need to obtain
the rest client instance from the handler or client group. Once you have the rest client,
you can retrieve the desired objects. For example:

```python
from asyncord.client_hub import connect
from asyncord.client.rest import RestClient

async def main():
    async with connect(API_TOKEN) as cli_group:
        # Getting the rest client instance
        rest_client = cli_group.client

        # Getting the guild and channel resources objects
        guild = await rest_client.guilds.get('guild_id')
        channel = await rest_client.channels.get('channel_id')
```
Here are some resources you can retrieve using the rest client:

- `guilds`
- `users`
- `channels`
- `applications`
- `interactions`
- `invites`
- `stage_instances`
- `webhooks`
- `auth`
- `stickers`
