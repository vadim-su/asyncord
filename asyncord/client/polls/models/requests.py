"""This module contains the response model for a polls."""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, Field, SerializerFunctionWrapHandler, field_serializer, model_validator

from asyncord.client.polls.models.common import PollLayoutType
from asyncord.snowflake import SnowflakeInputType

__all__ = (
    'Answer',
    'Poll',
    'PollEmoji',
)


class PollEmoji(BaseModel):
    """Represents a custom emoji that can be used in messages.

    Reference:
    https://discord.com/developers/docs/resources/emoji#emoji-object
    """

    id: SnowflakeInputType | None = None
    """Emoji id."""

    name: str | None = None
    """Emoji name."""

    @model_validator(mode='after')
    def validate_id_or_name(self) -> Self:
        """Validate that either id or name is set."""
        if not self.id and not self.name:
            raise ValueError('Either id or name must be set')

        if self.id and self.name:
            raise ValueError('Only one of id or name can be set')

        return self


class Answer(BaseModel):
    """Answer object.

    Answer object is not an actual discord object. It's media object but currently
    it uses only for answers. I removed media objects from question becauses it
    supports only text field.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-media-object-poll-media-object-structure
    """

    text: str = Field(max_length=300)
    """Text of the field.

    The maximum length of text is 300 for the question, and 55 for any answer.
    """

    emoji: PollEmoji | None = None
    """Partial Emoji object."""


class Poll(BaseModel):
    """Poll object.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-create-request-object
    """

    question: str = Field(max_length=300)
    """The question of the poll. Only text is supported.

    Under the hood, the question is a media object but it supports only text now.
    So, I decided to use a string field instead of a media object and prepare object
    for sending to the API in the serializer.
    """

    answers: list[Answer]
    """Each of the answers available in the poll."""

    duration: int | None = None
    """Number of hours the poll should be open for, up to 7 days."""

    allow_multiselect: bool
    """Whether a user can select multiple answers."""

    layout_type: PollLayoutType
    """The layout type of the poll."""

    @field_serializer('question', mode='wrap', when_used='json')
    @classmethod
    def serialize_question(
        cls,
        question: str,
        next_serializer: SerializerFunctionWrapHandler,
    ) -> dict[str, str]:
        """Prepare question for sending to the API.

        By default the question is wrapped in another structure. Currently for user
        it is overengineering to have a separate object for each question. I dicided
        to simplify the structure and allow user to pass a poll object directly.
        """
        serialized_question = next_serializer(question)
        return {'text': serialized_question}

    @field_serializer('answers', mode='wrap', when_used='json')
    @classmethod
    def serialize_answers(
        cls,
        answers: list[Answer],
        next_serializer: SerializerFunctionWrapHandler,
    ) -> list[dict[str, _JsonAnswerRepresentationType]]:
        """Prepare answers for sending to the API.

        By default the answers are wrapped in another structure. Currently for user
        it is overengineering to have a separate object for each answer. I dicided
        to simplify the structure and allow user to pass a list of poll media objects
        directly.
        """
        serialized_answers = next_serializer(answers)
        # fmt: off
        return [
            {'poll_media': answer}
            for answer in serialized_answers
        ]
        # fmt: on


type _JsonAnswerRepresentationType = dict[str, str | dict[str | None, str | None]]
