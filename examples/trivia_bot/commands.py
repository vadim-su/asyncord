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
    InteractionUpdateMessageData,
    InteractionUpdateMessageResponseRequest,
)

from asyncord.client.messages.models.requests.components import (
    ActionRow,
    Button,
    ButtonStyle,
)


class PollCommand:
    """Command to start a poll."""

    __command__ = CreateApplicationCommandRequest(
        name='poll',
        description='Poll example.',
    )
    __first_question__ = 'first_question_'
    __second_question__ = 'second_question_'
    __third_question__ = 'third_question_'

    def __init__(self) -> None:
        """Initialize the command."""
        self.answers = {}

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
        gateway.dispatcher.add_handler(InteractionCreateEvent, self.handle_answer)
        return command

    async def command(self, interaction: InteractionCreateEvent, client: RestClient) -> None:
        """Get the weather of a city."""
        if interaction.root.type != InteractionType.APPLICATION_COMMAND:
            return None
        if interaction.root.data.name != self.__command__.name:
            return None

        first_question = self._construct_question(
            'What is your favorite color?',
            ['Red', 'Blue', 'Green'],
            self.__first_question__,
        )

        return await client.interactions.send_response(
            interaction_id=interaction.root.id,
            interaction_token=interaction.root.token,
            interaction_response=InteractionChannelMessageResponsRequest(
                type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data=first_question,
            ),
        )

    async def handle_answer(
        self,
        interaction: InteractionCreateEvent,
        client: RestClient,
    ) -> None:
        """Handle the answer to questions."""
        if interaction.root.type != InteractionType.MESSAGE_COMPONENT:
            return None

        if interaction.root.data.custom_id.startswith(self.__first_question__):
            self.answers[self.__first_question__] = interaction.root.data.custom_id.split('_')[-1]
            message_data = self._construct_question(
                'What is your favorite animal?',
                ['Dog', 'Cat', 'Bird'],
                self.__second_question__,
                update=True,
            )
        elif interaction.root.data.custom_id.startswith(self.__second_question__):
            self.answers[self.__second_question__] = interaction.root.data.custom_id.split('_')[-1]
            message_data = self._construct_question(
                'What is your favorite food?',
                ['Pizza', 'Burger', 'Pasta'],
                self.__third_question__,
                update=True,
            )
        elif interaction.root.data.custom_id.startswith(self.__third_question__):
            self.answers[self.__third_question__] = interaction.root.data.custom_id.split('_')[-1]
            message_data = InteractionUpdateMessageData(
                content='Your answers are: \n' + '\n'.join([self.answers[key] for key in self.answers]),
            )
        else:
            return None

        return await client.interactions.send_response(
            interaction_id=interaction.root.id,
            interaction_token=interaction.root.token,
            interaction_response=InteractionUpdateMessageResponseRequest(
                type=InteractionResponseType.UPDATE_MESSAGE,
                data=message_data,
            ),
        )

    @classmethod
    def _construct_question(  # noqa
        cls,
        question: str,
        button_names: list[str],
        question_type: str,
        style: ButtonStyle = ButtonStyle.PRIMARY,
        update: bool = False,
    ) -> InteractionCreateMessageData:
        """Construct the action row."""
        components = cls._construct_buttons(
            button_names,
            question_type,
            style,
        )

        if update:
            return InteractionUpdateMessageData(
                content=question,
                components=[
                    ActionRow(
                        components=components,
                    ),
                ],
            )

        return InteractionCreateMessageData(
            content=question,
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
