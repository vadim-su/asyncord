"""This module contains all the necessary components related to OAuth2 authentication for Discord.

Reference:
https://discord.com/developers/docs/topics/oauth2
"""

from __future__ import annotations

from asyncord.client.applications.models.responses import ApplicationOut
from asyncord.client.auth.models import AuthorizationInfoResponse
from asyncord.client.resources import APIResource
from asyncord.typedefs import CURRENT_USER
from asyncord.urls import REST_API_URL

__all__ = ('OAuthResource',)


class OAuthResource(APIResource):
    """Represents an OAuth2 resource.

    It defines the OAuth2 resource that can be used to authenticate a user with Discord.

    In accordance with the relevant RFCs, the token and token revocation URLs will
    only accept a content type of application/x-www-form-urlencoded.
    JSON content is not permitted and will return an error.

    Reference:
    https://discord.com/developers/docs/topics/oauth2
    """

    oauth_url = REST_API_URL / 'oauth2'

    async def get_current_application_info(self) -> ApplicationOut:
        """Get the current application info.

        Reference:
        https://discord.com/developers/docs/topics/oauth2#get-current-bot-application-information
        """
        url = self.oauth_url / 'applications' / CURRENT_USER
        resp = await self._http_client.get(url=url)
        return ApplicationOut.model_validate(resp.body)

    async def get_current_authorization_info(self) -> AuthorizationInfoResponse:
        """Get the current authorization info.

        Reference:
        https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
        """
        url = self.oauth_url / CURRENT_USER
        resp = await self._http_client.get(url=url)
        return AuthorizationInfoResponse.model_validate(resp.body)
