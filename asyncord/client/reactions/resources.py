"""This module contains the ReactionResource class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncord.client.resources import APIResource
from asyncord.client.users.models.responses import UserResponse
from asyncord.typedefs import list_model
from asyncord.urls import REST_API_URL

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient
    from asyncord.snowflake import SnowflakeInputType

__all__ = ('ReactionResource',)


class ReactionResource(APIResource):
    """Reaction resource for a message.

    Attributes:
        channels_url: Base channels url.
    """

    channels_url = REST_API_URL / 'channels'

    def __init__(
        self,
        http_client: HttpClient,
        channel_id: SnowflakeInputType,
        message_id: SnowflakeInputType,
    ):
        """Initialize the reaction resource."""
        super().__init__(http_client)
        self.channel_id = channel_id
        messages_url = self.channels_url / str(self.channel_id) / 'messages'
        self.reactions_url = messages_url / str(message_id) / 'reactions'

    async def get(
        self,
        emoji: str,
        after: SnowflakeInputType | None = None,
        limit: int | None = None,
    ) -> list[UserResponse]:
        """Get a list of users that reacted with this emoji.

        Args:
            emoji: Emoji to get the reactions for.
            after: Get users after this user ID. Defaults to None.
            limit: Maximum number of users to return (1-100). Defaults to None.

        Returns:
            List of user which reacted with this emoji.
        """
        url_params = {}
        if after is not None:
            url_params['after'] = str(after)
        if limit is not None:
            url_params['limit'] = limit

        url = self.reactions_url / emoji % url_params
        resp = await self._http_client.get(url=url)
        return list_model(UserResponse).validate_python(resp.body)

    async def add(self, emoji: str) -> None:
        """Create a reaction for the message.

        Args:
            emoji: Emoji to react with.
        """
        url = self.reactions_url / emoji / '@me'
        await self._http_client.put(url=url)

    async def delete_own_reaction(self, emoji: str) -> None:
        """Delete a reaction the current user made for the message.

        Args:
            emoji: Emoji to delete the reaction for.
        """
        url = self.reactions_url / emoji / '@me'
        await self._http_client.delete(url=url)

    async def delete(
        self,
        emoji: str | None = None,
        user_id: SnowflakeInputType | None = None,
    ) -> None:
        """Delete a reaction a user made for the message.

        Args:
            emoji: Emoji to delete the reaction for.
            user_id: ID of the user to delete the reaction for.
        """
        if user_id and not emoji:
            raise ValueError('If user_id is specified, emoji must be specified too.')

        url = self.reactions_url
        if emoji is not None:
            url /= emoji
        if user_id is not None:
            url /= str(user_id)

        await self._http_client.delete(url=url)
