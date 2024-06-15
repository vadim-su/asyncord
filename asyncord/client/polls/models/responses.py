"""This module contains the response model for a polls."""

import datetime

from pydantic import BaseModel

from asyncord.client.polls.models.common import PollLayoutType
from asyncord.client.users.models.responses import UserResponse
from asyncord.snowflake import Snowflake


class GetAnswerVotersResponse(BaseModel):
    """Model for Get Answer Voters response.

    Reference:
    https://discord.com/developers/docs/resources/poll#get-answer-voters-response-body
    """

    users: list[UserResponse]


class PartialEmojiOut(BaseModel):
    """Represents a custom emoji that can be used in messages.

    Reference:
    https://discord.com/developers/docs/resources/emoji#emoji-object
    """

    id: Snowflake | None
    """Emoji id."""

    name: str | None
    """Emoji name.

    Can be null only in reaction emoji objects.
    """

    roles: list[Snowflake] | None = None
    """Roles allowed to use this emoji."""

    user: UserResponse | None = None
    """User that created this emoji."""

    require_colons: bool | None = None
    """Whether this emoji must be wrapped in colons."""

    managed: bool | None = None
    """Whether this emoji is managed."""

    animated: bool | None = None
    """Whether this emoji is animated."""

    available: bool | None = None
    """Whether this emoji can be used.

    May be false due to loss of Server Boosts.
    """


class PollMediaOut(BaseModel):
    """Poll Media Object.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-media-object-poll-media-object-structure
    """

    text: str | None = None
    """Text of the field."""

    emoji: PartialEmojiOut | None = None
    """Partial Emoji object."""


class PollAnswerOut(BaseModel):
    """Poll Answer Object.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-answer-object-poll-answer-object-structure
    """

    asnwer_id: int | None = None
    """ID of the answer."""

    poll_media: PollMediaOut
    """Data of the answer."""


class PollAnswerCountOut(BaseModel):
    """Model for Poll Answer Count Object.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-results-object-poll-answer-count-object-structure
    """

    id: int
    """ID of the answer."""

    count: int | None = None
    """Number of votes for this answer."""

    me_voted: bool
    """Whether the current user voted for this answer."""


class PollResultsOut(BaseModel):
    """Model for Poll Results Object.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-results-object-poll-results-object-structure
    """

    is_finalized: bool
    """Whether the votes have been precisely counted."""

    answer_count: list[PollAnswerCountOut] | None = None
    """Counts for each answer"""


class PollResponse(BaseModel):
    """Poll object.

    Reference:
    https://discord.com/developers/docs/resources/poll#poll-object-poll-object-structure
    """

    question: PollMediaOut
    """The question of the poll. Only text is supported."""

    answers: list[PollAnswerOut]
    """Each of the answers available in the poll."""

    expiry: datetime.datetime | None = None
    """The time when the poll ends."""

    allow_multiselect: bool
    """Whether a user can select multiple answers."""

    layout_type: PollLayoutType
    """The layout type of the poll."""

    results: PollResultsOut | None = None
    """The results of the poll."""
