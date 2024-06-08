"""This module contains the base classe for client resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncord.client.http.client import HttpClient


class APIResource:
    """Base class for client resources."""

    def __init__(self, http_client: HttpClient) -> None:
        """Initialize the resource.

        Args:
            http_client: HTTP client.
        """
        self._http_client = http_client
