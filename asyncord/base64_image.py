"""Base64 encoded image."""

import base64
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any, Self

import filetype
from pydantic import BaseModel
from pydantic_core import CoreSchema, core_schema


class Base64Image:
    """Base64 encoded image.

    data:image/jpeg;base64,BASE64_ENCODED_JPEG_IMAGE_DATA

    Reference:
    https://discord.com/developers/docs/reference#image-data
    """

    __slots__ = ('image_data',)

    def __init__(self, image_data: str) -> None:
        """Create new Base64Image object.

        Args:
            image_data: Base64 encoded image data.
        """
        self.image_data = image_data

    @classmethod
    def build(cls, image_data: bytes | str, image_type: str | None = None) -> Self:
        """Build Base64Image from separate parameters.

        Args:
            image_data: Image data.
            image_type: Image type.

        Returns:
            Base64Image object.

        Raises:
            ValueError: If image_data is not a valid image.
        """
        if isinstance(image_data, str):
            if not image_data.startswith('data:image/'):
                exc = ValueError('Icon must be a base64 encoded image')
                exc.add_note("If you're trying to use a file path, use `from_file` instead")
                raise exc
            return cls(image_data)

        if not image_type:
            guessed_image_type = filetype.guess(image_data)

            if not guessed_image_type:
                raise ValueError('Icon must be a valid image')

            image_type = guessed_image_type.mime

        encoded_image = base64.b64encode(image_data).decode()
        return cls(f'data:{image_type};base64, {encoded_image}')

    @classmethod
    def from_file(cls, file_path: str | Path) -> Self:
        """Build Base64Image from file path.

        Args:
            file_path: Path to file.

        Returns:
            Base64Image object.

        Raises:
            ValueError: If file_path is not a valid image.
        """
        with Path(file_path).open('rb') as file:
            return cls.build(file.read())

    @classmethod
    def validate(cls, value: bytes | str | Self) -> Self:
        """Pydantic auxiliary validation method.

        Args:
            value: Value to validate.

        Returns:
            Validated Base64Image.

        Raises:
            ValueError: If value is not
        """
        if isinstance(value, cls):
            return value

        if isinstance(value, bytes | str):
            return cls.build(value)

        if isinstance(value, Path):
            return cls.from_file(value)

        # This should never happen because of the pydantic schema
        raise ValueError('Invalid value type')  # pragma: no cover

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: type[BaseModel],
        _handler: Callable[[Any], CoreSchema],
    ) -> CoreSchema:
        """Pydantic auxiliary method to get schema.

        Args:
            _source: Source of schema.
            _handler: Handler of schema.

        Returns:
            Pydantic core schema.
        """
        schema = core_schema.union_schema([
            core_schema.bytes_schema(),
            core_schema.str_schema(),
            core_schema.is_instance_schema(Path),
            core_schema.is_instance_schema(cls),
        ])

        return core_schema.no_info_after_validator_function(
            function=cls.validate,
            schema=schema,
            serialization=core_schema.to_string_ser_schema(),
        )

    def __eq__(self, other: object) -> bool:
        """Compare image strings."""
        if isinstance(other, Base64Image):
            return self.image_data == other.image_data

        return super().__eq__(other)

    def __hash__(self) -> int:
        """Return the hash value of the image data."""
        return hash(self.image_data)

    def __str__(self) -> str:
        """Return image data."""
        return self.image_data


Base64ImageInputType = Annotated[Base64Image | bytes | str | Path, Base64Image]
"""Base64Image input type for pydantic models.

Base64ImageInput must validate and convert other types to Base64Image.
That's why we can't use just `Base64Image | bytes | str` as the type.
"""
