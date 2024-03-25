import abc  # noqa
import datetime
from typing import ClassVar

from asyncord.client.commands.models.requests import (
    AppCommandOptionType,
    ApplicationCommandStringOption,
    CreateApplicationCommandRequest,
)
from asyncord.client.commands.models.responses import ApplicationCommandResponse
from asyncord.client.interactions.models.common import InteractionResponseType, InteractionType
from asyncord.client.interactions.models.requests import (
    InteractionChannelMessageResponsRequest,
    InteractionCreateMessageData,
)
from asyncord.client.messages.models.requests.embeds import (
    Embed,
    EmbedAuthor,
    EmbedField,
    EmbedFooter,
    EmbedImage,
    EmbedThumbnail,
)
from asyncord.client.rest import RestClient
from asyncord.gateway.client.client import GatewayClient
from asyncord.gateway.events.interactions import InteractionCreateEvent
from asyncord.snowflake import SnowflakeInputType
from examples.weather_embed.models import WeatherOutput


class ChatCommand(abc.ABC):
    """Base class for chat commands."""

    __command__: ClassVar[CreateApplicationCommandRequest]

    @abc.abstractmethod
    async def command(
        self,
        interaction: InteractionCreateEvent,
        http_client: RestClient,
    ) -> None:
        """Command callback."""

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
        return command


class WeatherCommand(ChatCommand):
    """Command to get the weather."""

    __command__ = CreateApplicationCommandRequest(
        name='weather',
        description='Get the weather of a city.',
        options=[
            ApplicationCommandStringOption(
                type=AppCommandOptionType.STRING,
                name='city',
                description='The city to check the current weather in.',
                required=True,
            ),
        ],
    )

    def __init__(self, url: str, token: str) -> None:
        """Initialize the command."""
        self.weather_base_url = url
        self.weather_token = token

    async def command(self, interaction: InteractionCreateEvent, client: RestClient) -> None:
        """Get the weather of a city."""
        if interaction.root.type != InteractionType.APPLICATION_COMMAND:
            return
        if interaction.root.data.name != self.__command__.name:
            return

        url = f'{self.weather_base_url}{self.weather_token}&q={interaction.root.data.options[0].value}&aqi=no'
        try:
            output = await client._http_client.get(url)
        except TimeoutError as e:
            raise Exception('Request timed out.') from e

        weather = WeatherOutput.model_validate(output.body)

        embed = self._construct_embed(weather)

        action_row = InteractionCreateMessageData(
            embeds=[
                embed,
            ],
        )

        await client.interactions.send_response(
            interaction_id=interaction.root.id,
            interaction_token=interaction.root.token,
            interaction_response=InteractionChannelMessageResponsRequest(
                type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                data=action_row,
            ),
        )

    @classmethod
    def _construct_embed(cls, weather: WeatherOutput) -> Embed:
        """Construct the embed."""
        return Embed(
            title=f'Weather in {weather.location.name}',
            description=f'{weather.location.region}, {weather.location.country}',
            color=0x00FF00,
            fields=[
                EmbedField(
                    name='Temperature',
                    value=f'{weather.current.temp_c}°C',
                    inline=True,
                ),
                EmbedField(
                    name='Condition',
                    value=weather.current.condition.text,
                    inline=True,
                ),
                EmbedField(
                    name='Cloud',
                    value=f'{weather.current.cloud}%',
                    inline=True,
                ),
            ],
            thumbnail=EmbedThumbnail(
                url=f'https:{weather.current.condition.icon}',
            ),
            timestamp=datetime.datetime.now(),  # noqa
            author=EmbedAuthor(
                name='Weather',
                url='https://weatherapi.com',
            ),
            image=EmbedImage(
                url=f'https:{weather.current.condition.icon}',
            ),
            footer=EmbedFooter(
                text=f'Local Time: {weather.location.localtime}',
            ),
        )
