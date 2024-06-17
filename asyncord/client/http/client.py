"""Base asyncronous HTTP client."""

from __future__ import annotations

import asyncio
import logging
import warnings
from functools import partial
from typing import TYPE_CHECKING, Any

from asyncord.client.http.headers import HttpMethod
from asyncord.client.http.middleware.errors import ErrorHandlerMiddleware
from asyncord.client.http.models import FormField, FormPayload, JsonField, Request
from asyncord.client.http.request_handler import AiohttpRequestHandler

if TYPE_CHECKING:
    import aiohttp
    from pydantic import JsonValue

    from asyncord.client.http.middleware.base import Middleware, NextCallType
    from asyncord.client.http.models import Response
    from asyncord.client.http.request_handler import RequestHandler
    from asyncord.typedefs import StrOrURL


__all__ = ('HttpClient', 'make_payload_form')


logger = logging.getLogger(__name__)


class HttpClient:
    """Asyncronous HTTP client."""

    def __init__(
        self,
        session: aiohttp.ClientSession | object | None = None,
        request_handler: RequestHandler | None = None,
        middlewares: list[Middleware] | None = None,
    ) -> None:
        """Initialize the client.

        If no session is provided, requests will be made using the default session.
        When no request handler is provided, the default aiohttp request handler will be used.
        You should not provide both a session and a request handler at the same time because
        the session will be used only if no request handler is provided.

        Args:
            session: Client session. Defaults to None.
            request_handler: Request handler to use. Defaults to None.
            middlewares: Middlewares to apply. Defaults to None.
        """
        asyncio.get_running_loop()  # we want to make sure we are running in an event loop
        self.session = session
        self.middlewares: list[Middleware] = middlewares or []
        self.system_middlewares: list[Middleware] = [ErrorHandlerMiddleware()]

        if session and request_handler:
            warnings.warn(
                'You should not provide both a session and a request handler. Session will not be used.',
                stacklevel=2,
            )

        self._request_handler = request_handler or AiohttpRequestHandler(session)  # type: ignore

    async def get(
        self,
        *,
        url: StrOrURL,
        headers: dict[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a GET request.

        Args:
            url: URL to send the request to.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.GET,
                url=url,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    async def post(
        self,
        *,
        url: StrOrURL,
        payload: Any | None = None,  # noqa: ANN401
        headers: dict[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a POST request.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.POST,
                url=url,
                payload=payload,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    async def put(
        self,
        *,
        url: StrOrURL,
        payload: Any | None = None,  # noqa: ANN401
        headers: dict[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a PUT request.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.PUT,
                url=url,
                payload=payload,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    async def patch(
        self,
        *,
        url: StrOrURL,
        payload: Any,  # noqa: ANN401
        headers: dict[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a PATCH request.

        Args:
            url: URL to send the request to.
            payload: Payload to send with the request.
            files: Files to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.PATCH,
                url=url,
                payload=payload,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    async def delete(
        self,
        *,
        url: StrOrURL,
        payload: Any | None = None,  # noqa: ANN401
        headers: dict[str, str] | None = None,
        skip_middleware: bool = False,
    ) -> Response:
        """Send a DELETE request.

        Args:
            url: Url to send the request to.
            payload: Payload to send with the request. Defaults to None.
            headers: Headers to send with the request. Defaults to None.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Response:
            Response from the processed request.
        """
        return await self.request(
            Request(
                method=HttpMethod.DELETE,
                url=url,
                payload=payload,
                headers=headers or {},
            ),
            skip_middleware=skip_middleware,
        )

    def add_middleware(self, middleware: Middleware) -> None:
        """Add a middleware to the client.

        Args:
            middleware: Middleware to add.
        """
        self.middlewares.append(middleware)

    async def request(self, request: Request, *, skip_middleware: bool = False) -> Response:
        """Make a request to the Discord API.

        Args:
            request: Request data.
            skip_middleware: Whether to skip the middleware. Defaults to False.

        Returns:
            Response from the processed request.
        """
        if skip_middleware:
            return await self._request_handler.request(request)

        return await self._apply_middleware(request)

    async def _apply_middleware(self, request: Request) -> Response:
        """Apply middleware to the request.

        Args:
            request: Request data.

        Returns:
            Response from the processed request.
        """

        async def _request_wrap(
            request: Request,
            http_client: HttpClient,
        ) -> Response:
            """Wrap the request with middleware.

            It allows the request to be passed through the middleware stack and
            call at the end of the chain.
            """
            return await self._request_handler.request(request)

        middlewares = self.system_middlewares + list(reversed(self.middlewares))
        next_call: NextCallType = _request_wrap

        for middleware in middlewares:
            next_call = partial(middleware, next_call=next_call)

        return await next_call(request, self)


def make_payload_form(*, json_payload: JsonValue, **other_fields: FormField) -> FormPayload:
    """Make payload for a form request.

    Args:
        json_payload: Json payload to send.
        **other_fields: Other fields to send.

    Returns:
        Form payload.
    """
    fields: dict[str, FormField] = {}
    fields['payload_json'] = JsonField(value=json_payload)

    if other_fields:
        fields.update(other_fields)

    return FormPayload(fields)
