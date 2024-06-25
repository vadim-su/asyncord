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


@pytest.mark.parametrize('image_path', [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES])
def test_images_in_models_from_data(image_path: Path) -> None:
    """Test image convertation_to_base64_image from binary data."""

    class TestModel(BaseModel):
        image: Base64ImageInputType

    with image_path.open('rb') as file:
        image_data = file.read()
        model = TestModel(image=image_data)
        assert isinstance(model.image, Base64Image)


@pytest.mark.parametrize('image_path', [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES])
def test_images_in_models_from_pathes(image_path: Path) -> None:
    """Test image convertation_to_base64_image from pathes."""

    class TestModel(BaseModel):
        image: Base64ImageInputType

    model = TestModel(image=image_path)
    assert isinstance(model.image, Base64Image)


def test_base64_image_in_models_from_base64_image() -> None:
    """Test that base64 image can be passed to the model."""

    class TestModel(BaseModel):
        image: Base64ImageInputType

    image = Base64Image('data:image/png;base64,123')
    model = TestModel(image=image)
    assert model.image == image


def test_base64_image_error_in_models() -> None:
    """Test that error is raised if image is not base64 encoded."""

    class TestModel(BaseModel):
        image: Base64ImageInputType

    with pytest.raises(ValueError, match='Icon must be a base64 encoded image'):
        TestModel(image='not a base64 image')


def test_image_equal() -> None:
    """Test that images can be compared."""
    image1 = Base64Image('data:image/png;base64,123')
    image2 = Base64Image('data:image/png;base64,123')
    image3 = Base64Image('data:image/png;base64,124')

    assert image1 == image2
    assert image1 != image3
    assert image2 != image3


def test_image_hash() -> None:
    """Test that images can be hashed."""
    image1 = Base64Image('data:image/png;base64,123')
    image2 = Base64Image('data:image/png;base64,123')
    image3 = Base64Image('data:image/png;base64,124')

    assert hash(image1) == hash(image2)
    assert hash(image1) != hash(image3)


def test_image_to_str() -> None:
    """Test that images can be converted to string."""
    image = Base64Image('data:image/png;base64,123')
    assert str(image) == 'data:image/png;base64,123'
