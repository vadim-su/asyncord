"""This module contains the response model for a polls."""

from pydantic import BaseModel, Field, field_validator

from asyncord.client.polls.models.common import PollLayoutType
from asyncord.snowflake import Snowflake


class PartialEmoji(BaseModel):
    """Represents a custom emoji that can be used in messages.

    https://discord.com/developers/docs/resources/emoji#emoji-object
    """

    id: Snowflake | None
    """Emoji id."""

    name: str | None
    """Emoji name.

    Can be null only in reaction emoji objects.
    """


class PollMedia(BaseModel):
    """Poll Media Object.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-media-object-poll-media-object-structure
    """

    text: str = Field(None, max_length=300)
    """Text of the field.

    The maximum length of text is 300 for the question, and 55 for any answer.
    """

    emoji: PartialEmoji | None = None
    """Partial Emoji object."""


class PollAnswer(BaseModel):
    """Poll Answer Object.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-answer-object-poll-answer-object-structure
    """

    poll_media: PollMedia
    """Data of the answer."""

    @field_validator('poll_media')
    def validate_text_length(cls, poll_media: PollMedia) -> PollMedia:
        """Validate the text length."""
        max_length = 55

        if len(poll_media.text) > max_length:
            raise ValueError('Text length should be less than 55 characters.')
        return poll_media


class PollRequest(BaseModel):
    """Poll object.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-create-request-object
    """

    question: PollMedia
    """The question of the poll. Only text is supported."""

    answers: list[PollAnswer]
    """Each of the answers available in the poll."""

    duration: int | None = None
    """Number of hours the poll should be open for, up to 7 days."""

    allow_multiselect: bool
    """Whether a user can select multiple answers."""

    layout_type: PollLayoutType
    """The layout type of the poll."""

    @field_validator('question')
    def validate_text_length(cls, question: PollMedia) -> PollMedia:
        """Validate the text length."""
        max_length = 300

        if len(question.text) > max_length:
            raise ValueError('Text length should be less than 55 characters.')
        return question
