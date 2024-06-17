"""Request handler for the asyncord http client."""

from __future__ import annotations

import json
import logging
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Protocol

import aiohttp

from asyncord.client.http.headers import JSON_CONTENT_TYPE
from asyncord.client.http.models import FormPayload, Response

if TYPE_CHECKING:
    import io

    from asyncord.client.http.models import Request

__all__ = (
    'AiohttpRequestHandler',
    'RequestHandler',
)

logger = logging.getLogger(__name__)

MAX_BINARY_BODY_LOG_SIZE: Final[int] = 100
"""Maximum size of binary body to log."""


class RequestHandler(Protocol):
    """Request handler protocol."""

    async def request(self, request: Request) -> Response:
        """Make a raw request to the Discord API."""
        ...


class AiohttpRequestHandler:
    """Request handler using aiohttp.

    It's a default request handler for the asyncord http client.
    """

    def __init__(self, session: aiohttp.ClientSession | None = None):
        """Initialize the request handler.

        Args:
            session: Aiohttp client session.
        """
        self.session = session

    async def request(self, request: Request) -> Response:
        """Make a request.

        Args:
            request: Request object.

        Returns:
            Response object.
        """
        data, oppened_files = self._prepare_aiohttp_data_from_payload(request)
        try:
            return await self._make_raw_request(request, data)
        finally:
            for file in oppened_files:
                file.close()

    @classmethod
    def _prepare_aiohttp_data_from_payload(
        cls,
        request: Request,
    ) -> tuple[aiohttp.FormData | aiohttp.JsonPayload | None, list[io.BufferedReader]]:
        """Create aiohttp data from the payload.

        Args:
            request: Request object.

        Returns:
            Tuple of the raw data and the opened files.
        """
        match request.payload:
            case None:
                return None, []

            case FormPayload():
                data = aiohttp.FormData()
                oppened_files = []

                for name, field in request.payload:
                    value = field.serialize()

                    if isinstance(value, Path):
                        value = value.open('rb')
                        oppened_files.append(value)

                    data.add_field(
                        name=name,
                        value=value,
                        content_type=field.content_type,
                        filename=field.filename,
                    )
                return data, oppened_files

            case _:  # can't check for JsonValue because it's a type alias
                return aiohttp.JsonPayload(request.payload), []

    async def _make_raw_request(
        self,
        request: Request,
        data: aiohttp.FormData | aiohttp.JsonPayload | None,
    ) -> Response:
        """Make a raw request using aiohttp.

        Args:
            request: Request object.
            data: Data to send with the request.

        Returns:
            Response object.
        """
        request_conetxt = await self._create_request_context(request, data)
        async with request_conetxt as resp:
            return await self._transform_response(resp)

    async def _create_request_context(
        self,
        request: Request,
        prepared_data: aiohttp.FormData | aiohttp.JsonPayload | None,
    ) -> aiohttp.client._RequestContextManager | aiohttp.client._SessionRequestContextManager:
        """Create request's context."""
        if self.session:
            return self.session.request(
                method=request.method,
                url=request.url,
                data=prepared_data,
                headers=request.headers,
            )
        return aiohttp.request(
            method=request.method,
            url=request.url,
            data=prepared_data,
            headers=request.headers,
        )

    async def _transform_response(self, resp: aiohttp.ClientResponse) -> Response:
        """Transform aiohttp response to asyncord response."""
        return Response(
            raw_response=resp,
            status=HTTPStatus(resp.status),
            headers={header.lower(): value for header, value in resp.headers.items()},  # make all headers lowercase
            raw_body=await resp.read(),
            body=await self._extract_body_from_response(resp),
        )

    @classmethod
    async def _extract_body_from_response(cls, resp: aiohttp.ClientResponse) -> dict[str, Any]:
        """Extract the body from the response.

        Args:
            resp: Request response.

        Returns:
            Body of the parsed response.
        """
        if resp.status == HTTPStatus.NO_CONTENT:
            return {}

        if resp.headers.get('Content-Type') == JSON_CONTENT_TYPE:
            try:
                return await resp.json()
            except json.JSONDecodeError:
                body = await resp.read()
                if len(body) > MAX_BINARY_BODY_LOG_SIZE:
                    body = body[:MAX_BINARY_BODY_LOG_SIZE] + b'...'
                logger.warning('Failed to decode JSON body: %s', body)
                return {}

        return {}
