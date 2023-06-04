"""This module contains the ReactionResource class."""

from __future__ import annotations

from asyncord.client.models.users import User
from asyncord.client.resources import ClientResource, ClientSubresources
from asyncord.typedefs import LikeSnowflake, list_model
from asyncord.urls import REST_API_URL


class ReactionResource(ClientSubresources):
    """Reaction resource for a message.

    Attributes:
        channels_url (URL): Base channels url.
    """
    channels_url = REST_API_URL / 'channels'

    def __init__(
        self, parent: ClientResource, channel_id: LikeSnowflake, message_id: LikeSnowflake,
    ):
        """Initialize the reaction resource."""
        super().__init__(parent)
        self.channel_id = channel_id
        messages_url = self.channels_url / str(self.channel_id) / 'messages'
        self.reactions_url = messages_url / str(message_id) / 'reactions'

    async def get(
        self,
        emoji: str,
        after: LikeSnowflake | None = None,
        limit: int | None = None,
    ) -> list[User]:
        """Get a list of users that reacted with this emoji.

        Args:
            emoji (str): The emoji to get the reactions for.
            after (LikeSnowflake | None): Get users after this user ID.
                Defaults to None.
            limit (int | None): The maximum number of users to return (1-100).
                Defaults to None.

        Returns:
            list[User]: List of user which reacted with this emoji.
        """
        url_params = {}
        if after is not None:
            url_params['after'] = str(after)
        if limit is not None:
            url_params['limit'] = limit

        url = self.reactions_url / emoji % url_params
        resp = await self._http.get(url)
        return list_model(User).validate_python(resp.body)

    async def add(
        self,
        emoji: str,
    ) -> None:
        """Create a reaction for the message.

        Args:
            emoji (str): The emoji to react with.
            user_id (LikeSnowflake): The ID of the user to react as.
        """
        url = self.reactions_url / emoji / '@me'
        await self._http.put(url, None)

    async def delete_own_reaction(self, emoji: str) -> None:
        """Delete a reaction the current user made for the message.

        Args:
            emoji (str): The emoji to delete the reaction for.
        """
        url = self.reactions_url / emoji / '@me'
        await self._http.delete(url)

    async def delete(
        self,
        emoji: str | None = None,
        user_id: LikeSnowflake | None = None,
    ) -> None:
        """Delete a reaction a user made for the message.

        Args:
            emoji (str | None): The emoji to delete the reaction for.
            user_id (LikeSnowflake | None): The ID of the user to delete the reaction for.
        """
        if user_id and not emoji:
            raise ValueError('If user_id is specified, emoji must be specified too.')

        url = self.reactions_url
        if emoji is not None:
            url /= emoji
        if user_id is not None:
            url /= str(user_id)

        await self._http.delete(url)
