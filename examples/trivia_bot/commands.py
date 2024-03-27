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


from asyncord.client.interactions.models.requests import (
    InteractionChannelMessageResponsRequest,
    InteractionCreateMessageData,
)
from asyncord.client.messages.models.requests.components import (
    ActionRow,
    Button,
    ButtonStyle,
)


class PollCommand:
    """Command to start a poll."""

    __command__ = CreateApplicationCommandRequest(
        name='weather',
        description='Get the weather of a city.',
    )
    __first_question__ = 'first_question'
    __second_question__ = 'second_question'
    __third_question__ = 'third_question'

    def __init__(self, url: str, token: str) -> None:
        """Initialize the command."""
        self.weather_base_url = url
        self.weather_token = token

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
        gateway.dispatcher.add_handler(InteractionCreateEvent, self.handle_first_question)
        gateway.dispatcher.add_handler(InteractionCreateEvent, self.handle_second_question)
        gateway.dispatcher.add_handler(InteractionCreateEvent, self.handle_third_question)
        return command

    async def command(self, interaction: InteractionCreateEvent, client: RestClient) -> None:
        """Get the weather of a city."""
        if interaction.root.type != InteractionType.APPLICATION_COMMAND:
            return None
        if interaction.root.data.name != self.__command__.name:
            return None

        first_question = self._construct_first_question()

        return await client.interactions.send_response(
            interaction_id=interaction.root.id,
            interaction_token=interaction.root.token,
            interaction_response=InteractionChannelMessageResponsRequest(
                type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data=first_question,
            ),
        )

    async def handle_first_question(
        self,
        interaction: InteractionCreateEvent,
        client: RestClient,
    ) -> None:
        """Handle the first question."""
        if interaction.root.type != InteractionType.APPLICATION_COMMAND:
            return
        if interaction.root.data.name != self.__command__.name:
            return

        return

    @classmethod
    def _construct_first_question(
        cls,
    ) -> InteractionCreateMessageData:
        """Construct the action row."""
        button_names = ['London', 'Paris', 'Tokyo']

        components = cls._construct_buttons(
            button_names,
            cls.__first_question__,
        )

        return InteractionCreateMessageData(
            content="What's your city?",
            components=[
                ActionRow(
                    components=components,
                ),
            ],
        )

    @classmethod
    def _construct_second_question(
        cls,
    ) -> InteractionCreateMessageData:
        """Construct the action row."""
        button_names = ['London', 'Paris', 'Tokyo']

        components = cls._construct_buttons(
            button_names,
            cls.__first_question__,
        )

        return InteractionCreateMessageData(
            content="What's your city?",
            components=[
                ActionRow(
                    components=components,
                ),
            ],
        )

    @classmethod
    def _construct_buttons(
        cls,
        buttons: list[str],
        question_type: str,
        style: ButtonStyle = ButtonStyle.PRIMARY,
    ) -> list[Button]:
        """Construct the action row."""
        components = []
        for button in buttons:
            components.append(
                Button(
                    style=style,
                    label=button,
                    custom_id=question_type + button,
                ),
            )

        return components
