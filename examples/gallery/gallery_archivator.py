"""This example demonstrates how to create a gallery archivator using Asyncord.

It uses the rest client to get the threads in the guild and then archives them if they are in the gallery channel.
"""

import asyncio
import logging
import os

from dotenv import load_dotenv

from asyncord.client.rest import RestClient
from asyncord.snowflake import SnowflakeInputType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
API_TOKEN: str = os.getenv('API_TOKEN')  # type: ignore
FORUM_CHANNEL_ID: str = os.getenv('FORUM_CHANNEL_ID')  # type: ignore
GUILD_ID: str = os.getenv('GUILD_ID')  # type: ignore


class GalleryArchivator:
    """Archivator of old posts in the gallery."""

    def __init__(
        self,
        run_period: int,
        client: RestClient,
        gallery_channel_id: SnowflakeInputType,
        guild_id: SnowflakeInputType,
    ) -> None:
        """Initialize the processor with a given period in seconds."""
        self.run_period = run_period
        self.client = client
        self.gallery_channel_id = gallery_channel_id
        self.guild_id = guild_id

    async def run(self) -> None:
        """Run the handler in a loop with a given period."""
        while True:
            logger.info('Running acrhivator handler')
            await self.handler()
            await asyncio.sleep(self.run_period)

    async def handler(self) -> None:
        """Handle the gallery archivation."""
        # Get the gallery channel
        guild_threads_resp = await self.client.guilds.get_active_threads(self.guild_id)

        threads_to_process = []

        for thread in guild_threads_resp.threads:
            if thread.parent_id != self.gallery_channel_id:
                continue
            if thread.thread_metadata.archived:
                continue

            threads_to_process.append(thread)

        for thread in threads_to_process:
            # we can add more conditions here
            # for example, we can check the last message timestamp
            # and archive the thread if it's older than 1 month
            await self.client.channels.threads(self.guild_id).archive(thread.id)


async def main() -> None:
    """Run the main function."""
    client = RestClient(API_TOKEN)

    processor = GalleryArchivator(
        run_period=30,
        client=client,
        gallery_channel_id=FORUM_CHANNEL_ID,
        guild_id=GUILD_ID,
    )
    await processor.run()


if __name__ == '__main__':
    asyncio.run(main())
