"""Example of using OpenAI API to analyze forum threads and determine their tags.

This example demonstrates how to add custom variables to the handler function on interaction
with OpenAI API. The example uses the OpenAI API to analyze forum threads and determine their tags.
"""

from __future__ import annotations

import asyncio
import enum
import logging
import os
from typing import Self

from dotenv import load_dotenv
from openai import AsyncOpenAI, BaseModel, pydantic_function_tool
from pydantic import Field

from asyncord.client.channels.models.requests.updating import UpdateChannelRequest
from asyncord.client.rest import RestClient
from asyncord.client_hub import ClientHub
from asyncord.gateway.events.channels import ThreadCreateEvent
from asyncord.snowflake import SnowflakeInputType

load_dotenv()
API_TOKEN: str = os.getenv('API_TOKEN')  # type: ignore
OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')  # type: ignore
FORUM_CHANNEL_ID: str = os.getenv('FORUM_CHANNEL_ID')  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYS_PROMPT = """
You are analyzing a forum thread to determine its tags.
The thread is about a question, an issue, or someone needing help.
The tags can be one or more.
"""

LLM_MODEL = 'gpt-4o'


@enum.unique
class TagEnum(enum.StrEnum):
    """Enum with a snowflake tag id."""

    tag_id: SnowflakeInputType
    """Enum with a snowflake tag id."""

    def __new__(cls, value: str, snowflake: SnowflakeInputType) -> Self:
        """Create a new instance of the enum."""
        obj = str.__new__(cls)
        obj._value_ = value
        obj.tag_id = snowflake
        return obj

    QUESTION = ('question', '1306195772378972221')
    """Question tag id."""

    ISSUE = ('issue', '1306195838489333771')
    """Issue tag id."""

    NEED_HELP = ('NeedHelp', '1306195901584511006')
    """Need help tag id."""


class TagLlmValidator(BaseModel, extra='forbid'):
    """Validator for the tags."""

    tags: list[TagEnum] = Field(description='Tags for the thread')


async def analyze_thread(title: str | None, content: str | None, ai_client: AsyncOpenAI) -> set[TagEnum]:
    """Analyze the thread.

    Args:
        title: The title of the thread.
        content: The content of the thread.
        ai_client: The OpenAI client.

    Returns:
        List of tags for the thread.
    """
    user_request = f"""
    Title:
    {title}

    Content:
    {content}
    """

    # We ask the model to predict the tags for the thread
    # System prompt is used to set rules for the model
    # User prompt is the input that the model will analyze
    messages = [
        {'role': 'system', 'content': SYS_PROMPT},
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': user_request},
            ],
        },
    ]

    # We define the tools that the model will use to analyze the thread
    # In this case, we use the TagLlmValidator to validate the tags and get pydantic model
    # instead of raw text
    tools = [
        pydantic_function_tool(
            TagLlmValidator,
            name='Tags',
            description='Tags for the thread',
        ),
    ]

    # Request the model to predict the tags for the thread
    # and extract the tags from the result
    completion = await ai_client.beta.chat.completions.parse(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.5,
        max_completion_tokens=500,
        tools=tools,
        tool_choice='required',  # we want the model to use the tools always
    )
    tool_calls = completion.choices[0].message.tool_calls
    llm_result: TagLlmValidator = tool_calls[0].function.parsed_arguments  # type: ignore

    return set(llm_result.tags)


async def on_thread_created(
    event: ThreadCreateEvent,
    client: RestClient,
    ai_client: AsyncOpenAI,
) -> None:
    """Handle the thread creation event."""
    if event.parent_id != FORUM_CHANNEL_ID:
        return

    title = event.name
    content = None

    # Retrieve the text of the forum post
    # This is done by fetching the message from the thread channel itself
    # The channel ID and message ID are identical (:
    messages_res = client.channels.messages(event.id)
    message = await messages_res.get(around=event.id, limit=1)
    if message:
        content = message[0].content[:100]
    else:
        # it should be unreachable, but just in case
        logger.error('Weird, no message found for the thread')

    # This condition is to prevent empty threads from being analyzed
    # but in real life it shouldn't happen
    if not title and not content:
        logger.warning('No title or content found in the thread')
        return

    # Analyze the thread and get the predicted tags
    predicted_tags = await analyze_thread(title, content, ai_client)
    # Add the predicted tags to already applied tags
    tags = [tag.tag_id for tag in predicted_tags] + (event.applied_tags or [])

    await client.channels.update(
        event.id,
        channel_data=UpdateChannelRequest(applied_tags=tags),
    )


async def main() -> None:
    """Run the main function."""
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async with ClientHub.connect(API_TOKEN) as client_group:
        # This is the way to add custom arguments to handlers
        # It processes the arguments and passes them to the handler by name
        client_group.dispatcher.add_argument('ai_client', openai_client)
        client_group.dispatcher.add_handler(on_thread_created)


if __name__ == '__main__':
    asyncio.run(main())
