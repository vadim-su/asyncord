import aiohttp

from asyncord.client.commands import CreateApplicationCommandData
from asyncord.client.models.activity import Activity, ActivityType
from asyncord.client.models.commands import ApplicationCommandType
from asyncord.client.rest import RestClient
from asyncord.gateway.client import AsyncGatewayClient
from asyncord.gateway.commands import PresenceUpdateData
from asyncord.gateway.events.base import ReadyEvent

API_TOKEN = 'OTI5NjUxNjgwNjUwMzQyNDEy.GPAIC9.u-m5k577Ck9DmOCk2RX6UFZBkGlsREQBF2IsS8'
APP_ID = 929651680650342412

DEFAULT_ACTIVITY = Activity(
    type=ActivityType.GAME,
    name='with you',
    details="I'm playing a game",
)


async def main():
    async with aiohttp.ClientSession() as session:
        gw = AsyncGatewayClient(API_TOKEN, session=session)
        client = RestClient(API_TOKEN)
        client._http._session = session
        gw.dispatcher.add_argument('client', client)

        async def on_ready(_: ReadyEvent, gateway: AsyncGatewayClient):
            await gw.update_presence(PresenceUpdateData(
                activities=[DEFAULT_ACTIVITY],
            ))

            await client.applications.commands(APP_ID).create(
                CreateApplicationCommandData(
                    type=ApplicationCommandType.CHAT_INPUT,
                    name="ping",
                    description="Should return Pong!",
                ))

        gw.add_handler(on_ready)

        await gw.start()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
