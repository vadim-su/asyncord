import aiohttp  # noqa

from asyncord.client.rest import RestClient
from asyncord.gateway.client.client import GatewayClient
from asyncord.gateway.events.base import ReadyEvent
from examples.weather_embed.commands import WeatherCommand

API_TOKEN = ''
APP_ID = ''

WEATHER_TOKEN = ''
WEATHER_URL = 'https://api.weatherapi.com/v1/current.json?key='


async def main() -> None:
    """Run the bot."""
    async with aiohttp.ClientSession() as session:
        gw = GatewayClient(
            token=API_TOKEN,
            session=session,
        )
        client = RestClient(API_TOKEN)
        client._http_client._session = session
        gw.dispatcher.add_argument('client', client)
        gw.dispatcher.add_argument('gateway', gw)

        async def on_ready(
            ready_event: ReadyEvent,
            gateway: GatewayClient,
            client: RestClient,
        ) -> None:
            await WeatherCommand().register(gateway, client, APP_ID)

        gw.dispatcher.add_handler(on_ready)
        await gw.connect()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
