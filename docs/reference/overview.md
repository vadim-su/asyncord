# Overview

## Project Structure

The `asyncord` project is organized into several key modules, each responsible for different aspects of the library.
The `client` module handles client-side operations and resources, while the `gateway` module manages the connection
to the Discord Gateway. Additional utility modules provide logging, type definitions, and URL management, ensuring
a well-structured and maintainable codebase.

## Resource General Structure

Resources in Asyncord follow a general structure that includes the following components:

- **Resource** (e.g., `ChannelResource`): Represents a specific Discord resource, such as a channel, user, or message. Resources are responsible for managing the data associated with the resource and interacting with the Discord API to perform operations.

- **Models**: Represents the data structure of the resource. Models define the fields and properties associated with the resource and provide methods for data validation and serialization. Can be splitted into `requests` and `responses` models. Also can contain super general models in `common` module.

In general, the structure of a resource module looks like this:

```plaintext
    asyncord/client/resource
    ├── models
    │   ├── common.py
    │   ├── requests.py
    │   └── responses.py
    └── resources.py
```

but in specific cases, the structure can be more complex in depth. Look at the examples below.

??? example "Simple Resource Structure"

    ```plaintext
        asyncord/client/guilds
        ├── models
        │   ├── common.py
        │   ├── requests.py
        │   └── responses.py
        └── resources.py
    ```

??? example "Complex Resource Structure"

    ```plaintext
    asyncord/client/messages
    ├── models
    │   ├── common.py
    │   ├── requests
    │   │   ├── base_message.py
    │   │   ├── components
    │   │   │   ├── action_row.py
    │   │   │   ├── base.py
    │   │   │   ├── buttons.py
    │   │   │   ├── emoji.py
    │   │   │   ├── selects.py
    │   │   │   └── text_input.py
    │   │   ├── embeds.py
    │   │   └── messages.py
    │   └── responses
    │       ├── components.py
    │       ├── embeds.py
    │       └── messages.py
    └── resources.py
    ```

## Modules Overview

### `asyncord` (root)
| Module               | Description                                                    |
| :------------------- | :------------------------------------------------------------- |
| `base64_image.py`    | Utilities for handling base64 encoded images.                  |
| `client_hub.py`      | Manages multiple clients with the `ClientHub` class.           |
| `color.py`           | Utilities for handling color values.                           |
| `locale.py`          | Utilities and definitions for handling locales.                |
| `snowflake.py`       | Utilities for handling Discord snowflakes.                     |

### `client`
| Module               | Description                                                       |
| :------------------- | :---------------------------------------------------------------- |
| `applications`       | Resources and models related to Discord applications.             |
| `bans`               | Resources and models related to bans.                             |
| `channels`           | Resources and models related to channels.                         |
| `commands`           | Resources and models related to commands.                         |
| `emojis`             | Resources and models related to emojis.                           |
| `guild_templates`    | Resources and models related to guild templates.                  |
| `guilds`             | Resources and models related to guilds.                           |
| `http`               | Base HTTP client and middleware for handling requests.            |
| `interactions`       | Resources and models related to interactions.                     |
| `invites`            | Resources and models related to invites.                          |
| `members`            | Resources and models related to members.                          |
| `messages`           | Resources and models related to messages.                         |
| `polls`              | Resources and models related to polls.                            |
| `rest.py`            | REST client for Asyncord.                                         |
| `roles`              | Resources and models related to roles.                            |
| `scheduled_events`   | Resources and models related to scheduled events.                 |
| `stage_instances`    | Resources and models related to stage instances.                  |
| `stickers`           | Resources and models related to stickers.                         |
| `threads`            | Resources and models related to threads.                          |
| `users`              | Resources and models related to users.                            |
| `webhooks`           | Resources and models related to webhooks.                         |

### `gateway`
| Module         | Description                                              |
| :------------- | :------------------------------------------------------- |
| `commands.py`  | Models for the commands sent to the gateway.             |
| `events`       | Event models for the gateway.                            |
| `intents.py`   | Intent models for the gateway.                           |

### Other Modules
| Module        | Description                                                 |
| :------------ | :---------------------------------------------------------- |
| `logger.py`   | Logging utilities for Asyncord.                             |
| `typedefs.py` | Type definitions used throughout the project.               |
| `urls.py`     | Base URLs for the Discord API and Gateway.                  |
