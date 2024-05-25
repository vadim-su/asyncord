from pathlib import Path

import pytest
from pydantic import BaseModel

from asyncord.base64_image import Base64Image, Base64ImageInputType

TEST_FILE_NAMES = ['test_image_1.png', 'test_image_2.png']


@pytest.mark.parametrize('img_name', [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES])
def test_images_from_files(img_name: Path) -> None:
    """Test that images can be created from files."""
    enc_image = Base64Image.from_file(img_name)
    assert enc_image.image_data.startswith('data:image/')
    assert ';base64,' in enc_image.image_data
    assert len(enc_image.image_data) > 100


@pytest.mark.parametrize('img_name', [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES])
def test_build_image(img_name: Path) -> None:
    """Test that images can be built from binary data."""
    with Path(img_name).open('rb') as file:
        enc_image = Base64Image.build(file.read())
    assert enc_image.image_data.startswith('data:image/')
    assert ';base64,' in enc_image.image_data
    assert len(enc_image.image_data) > 100


@pytest.mark.parametrize('img_name', [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES])
def test_base64_images_in_models(img_name: Path) -> None:
    """Test that images can be used in pydantic models."""

    class TestModel(BaseModel):
        image: Base64ImageInputType

    with Path(img_name).open('rb') as file:
        image_data = file.read()
        model = TestModel(image=image_data)
        assert isinstance(model.image, Base64Image)


def test_base64_image_error_in_models() -> None:
    """Test that images can be used in pydantic models."""

    class TestModel(BaseModel):
        image: Base64ImageInputType

    with pytest.raises(ValueError, match='Icon must be a base64 encoded image'):
        TestModel(image='not a base64 image')
