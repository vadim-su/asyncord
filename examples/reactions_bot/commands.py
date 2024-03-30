import abc  # noqa

from asyncord.client.commands.models.requests import (
    CreateApplicationCommandRequest,
)
from asyncord.client.commands.models.responses import ApplicationCommandResponse
from asyncord.client.interactions.models.common import InteractionResponseType, InteractionType

from asyncord.client.rest import RestClient
from asyncord.gateway.client.client import GatewayClient
from asyncord.gateway.events.interactions import InteractionCreateEvent
from asyncord.snowflake import SnowflakeInputType

from asyncord.client.messages.models.common import MessageFlags
from asyncord.client.interactions.models.requests import (
    InteractionChannelMessageResponsRequest,
    InteractionCreateMessageData,
)

from asyncord.gateway.events.messages import (
    MessageReactionAddEvent,
    MessageReactionRemoveEvent,
)


from asyncord.client.messages.models.requests.components import (
    ActionRow,
    Button,
    ButtonStyle,
)


REACTIONS = ['👍', '👎', '🤷']


class ReactionsCommand:
    """Command to start reaction example."""

    __command__ = CreateApplicationCommandRequest(
        name='reactions',
        description='Reactions menu.',
    )

    __custom_id__ = 'button_'

    def __init__(self, app_id: str) -> None:
        """Initialize the command."""
        self.bot_id = app_id

    async def register(
        self,
        gateway: GatewayClient,
        client: RestClient,
        app_id: SnowflakeInputType,
    ) -> ApplicationCommandResponse:
        """Register the command to the client."""
        command_res = client.applications.commands(app_id)
        command = await command_res.create(self.__command__)
        gateway.dispatcher.add_handler(InteractionCreateEvent, self.command)
        gateway.dispatcher.add_handler(InteractionCreateEvent, self.handle_buttons)
        gateway.dispatcher.add_handler(MessageReactionAddEvent, self.handle_reaction)
        gateway.dispatcher.add_handler(MessageReactionRemoveEvent, self.handle_remove_reaction)

        return command

    async def command(self, interaction: InteractionCreateEvent, client: RestClient) -> None:
        """Get the weather of a city."""
        if interaction.root.type != InteractionType.APPLICATION_COMMAND:
            return None
        if interaction.root.data.name != self.__command__.name:
            return None

        buttons = [
            Button(
                style=ButtonStyle.PRIMARY,
                label=reaction,
                custom_id=self.__custom_id__ + reaction,
            )
            for reaction in REACTIONS
        ]

        message = InteractionCreateMessageData(
            content='This is a reactions example.\n'
            + 'Click buttons to make bot react to this message.\n'
            + 'Add reactions to make this bot react to the reactions.',
            components=[
                ActionRow(
                    components=buttons,
                ),
            ],
        )

        return await client.interactions.send_response(
            interaction_id=interaction.root.id,
            interaction_token=interaction.root.token,
            interaction_response=InteractionChannelMessageResponsRequest(
                type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data=message,
            ),
        )

    async def handle_buttons(
        self,
        interaction: InteractionCreateEvent,
        client: RestClient,
    ) -> None:
        """Handle the button clicks.

        Puts a corresponding reaction to the message.
        """
        if interaction.root.type != InteractionType.MESSAGE_COMPONENT:
            return None

        if not interaction.root.data.custom_id.startswith(self.__custom_id__):
            return None

        reaction_res = client.channels.messages(
            interaction.root.message.channel_id,
        ).reactions(
            interaction.root.message.id,
        )

        reacted_users = await reaction_res.get(
            emoji=interaction.root.data.custom_id.split('_')[-1],
        )

        if any(user.id == self.bot_id for user in reacted_users):
            await reaction_res.delete_own_reaction(
                emoji=interaction.root.data.custom_id.split('_')[-1],
            )
            content = 'You made bot remove reaction ' + interaction.root.data.custom_id.split('_')[-1]
        else:
            await reaction_res.add(
                emoji=interaction.root.data.custom_id.split('_')[-1],
            )

            content = 'You made bot react with ' + interaction.root.data.custom_id.split('_')[-1]

        return await client.interactions.send_response(
            interaction_id=interaction.root.id,
            interaction_token=interaction.root.token,
            interaction_response=InteractionChannelMessageResponsRequest(
                type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data=InteractionCreateMessageData(
                    content=content,
                    flags=MessageFlags.EPHEMERAL,
                ),
            ),
        )

    async def handle_reaction(
        self,
        add_event: MessageReactionAddEvent,
        client: RestClient,
    ) -> None:
        """Handle the reactions addition.

        Sends an ephemerial message when user reacts to the message.
        """
        if add_event.user_id == self.bot_id:
            return None

        message_res = client.channels.messages(
            add_event.channel_id,
        )

        messages = await message_res.get(
            around=add_event.message_id,
            limit=1,
        )

        if messages[0].author.id != self.bot_id:
            return None

        return await message_res.create(
            message_data=InteractionCreateMessageData(
                content='You added reaction ' + add_event.emoji.name,
                flags=MessageFlags.EPHEMERAL,
            ),
        )

    async def handle_remove_reaction(
        self,
        remove_event: MessageReactionRemoveEvent,
        client: RestClient,
    ) -> None:
        """Handle the reactions removal.

        Sends an ephemerial message when user reacts to the message.
        """
        if remove_event.user_id == self.bot_id:
            return None

        message_res = client.channels.messages(
            remove_event.channel_id,
        )

        messages = await message_res.get(
            around=remove_event.message_id,
            limit=1,
        )

        if messages[0].author.id != self.bot_id:
            return None

        return await message_res.create(
            message_data=InteractionCreateMessageData(
                content='You removed reaction ' + remove_event.emoji.name,
                flags=MessageFlags.EPHEMERAL,
            ),
        )
