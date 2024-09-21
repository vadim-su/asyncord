"""This module provides custom URL types and constraints for use with Pydantic models."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Annotated, Any, Self

import yarl
from pydantic import AnyUrl, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

from asyncord.typedefs import StrOrURL

__all__ = (
    'AttachmentUrl',
    'HttpYarlUrl',
    'YarlUrl',
    'YarlUrlConstraint',
    'YarlUrlType',
)


class YarlUrl:
    """Yarl url field type for Pydantic models."""

    __slots__ = ('raw_url',)

    def __init__(self, url: str | yarl.URL) -> None:
        """URL object."""
        self.raw_url = yarl.URL(url)

    @classmethod
    def validate(cls, value: str | yarl.URL | StrOrURL | AnyUrl | Self) -> Self:
        """Pydantic auxiliary validation method.

        Args:
            value: Value to validate.
            _validation_info: Validation information.

        Returns:
            Validated url.
        """
        if isinstance(value, cls):
            return value

        if isinstance(value, str | yarl.URL):
            return cls(value)

        if isinstance(value, AnyUrl):
            return cls(str(value))

        raise ValueError(f'Invalid URL type: {type(value)}')

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: type[Self],
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Pydantic auxiliary method to get schema.

        Args:
            _source_type: Source of schema.
            _handler: Handler of schema.

        Returns:
            Pydantic core schema.
        """
        json_schema = core_schema.no_info_after_validator_function(
            function=cls,
            schema=core_schema.url_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

        python_schema = core_schema.no_info_after_validator_function(
            function=cls,
            schema=core_schema.union_schema([
                core_schema.is_instance_schema(cls),
                core_schema.is_instance_schema(yarl.URL),
                core_schema.is_instance_schema(AnyUrl),
                core_schema.str_schema(),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                function=lambda inst: inst.raw_url,
            ),
        )

        return core_schema.json_or_python_schema(
            json_schema=json_schema,
            python_schema=python_schema,
            serialization=core_schema.to_string_ser_schema(when_used='json-unless-none'),
        )

    def __str__(self) -> str:
        """Return URL as string."""
        return str(self.raw_url)

    def __len__(self) -> int:
        """Return length of URL."""
        return len(str(self.raw_url))

    def __repr__(self) -> str:
        """Return URL - like object representation."""
        return f'<{self.__class__.__name__} url={self.raw_url!r}>'

    def __eq__(self, other: object) -> bool:
        """Check if URLs are equal."""
        if isinstance(other, YarlUrl):
            return self.raw_url == other.raw_url

        return super().__eq__(other)

    def __hash__(self) -> int:
        """Return hash of URL."""
        return hash(self.raw_url)


type YarlUrlType = Annotated[str | yarl.URL | AnyUrl | YarlUrl, YarlUrl]
"""Yarl URL type for Pydantic models.

It fix a problem with mypy and pylance errors when using yarl.URL|str and any url in Pydantic models.
"""


@dataclass(frozen=True)
class YarlUrlConstraint:
    """Yarl URL constraint for Pydantic models."""

    max_length: int | None = None
    """Maximum length of URL."""

    allowed_schemes: Iterable[str] | None = None
    """Allowed URL schemes."""

    def validate_url(self, url: YarlUrl) -> YarlUrl | yarl.URL:
        """Validate URL.

        Args:
            url: URL to validate.

        Returns:
            Validated URL.

        Raises:
            ValueError: If URL is invalid.

        """
        if self.max_length and len(url) > self.max_length:
            raise ValueError(f'URL is too long: {url}')

        if self.allowed_schemes and url.raw_url.scheme not in self.allowed_schemes:
            raise ValueError(f'Invalid URL scheme: {url.raw_url.scheme}')

        return url

    def __get_pydantic_core_schema__(
        self,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Pydantic auxiliary method to get schema.

        Args:
            source_type: Source of schema.
            handler: Handler of schema.

        Returns:
            Pydantic core schema.
        """
        return core_schema.no_info_after_validator_function(
            function=self.validate_url,
            schema=handler(source_type),
        )


type HttpYarlUrl = Annotated[
    YarlUrlType,
    YarlUrlConstraint(max_length=2000, allowed_schemes={'http', 'https'}),
]
"""HTTP Yarl URL type for Pydantic models."""

type AttachmentUrl = Annotated[YarlUrlType, YarlUrlConstraint(allowed_schemes={'attachment'})]
"""Special type for attachment URLs."""
