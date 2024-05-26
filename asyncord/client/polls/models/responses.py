"""This module contains the response model for a polls."""

from pydantic import BaseModel

from asyncord.client.users.models.responses import UserResponse


class GetAnswerVotersResponse(BaseModel):
    """Model for Get Answer Voters response.

    Reference:
    https://canary.discord.com/developers/docs/resources/poll#get-answer-voters-response-body
    """

    users: list[UserResponse]
