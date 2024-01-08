
from pathlib import Path

import pytest
from pydantic import BaseModel

from asyncord.base64_image import Base64Image, Base64ImageInputType

TEST_FILE_NAMES = ['test_image_1.png', 'test_image_2.jpg']


@pytest.mark.parametrize('img_name', [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES])
def test_images_from_files(img_name: Path):
    enc_image = Base64Image.from_file(img_name)
    assert enc_image.image_data.startswith('data:image/')
    assert ';base64,' in enc_image.image_data
    assert len(enc_image.image_data) > 100


@pytest.mark.parametrize('img_name', [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES])
def test_build_image(img_name: Path):
    with open(img_name, 'rb') as file:
        enc_image = Base64Image.build(file.read())
    assert enc_image.image_data.startswith('data:image/')
    assert ';base64,' in enc_image.image_data
    assert len(enc_image.image_data) > 100


@pytest.mark.parametrize('img_name', [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES])
def test_base64_images_in_models(img_name: Path):
    class TestModel(BaseModel):
        image: Base64ImageInputType

    with open(img_name, 'rb') as file:
        image_data = file.read()
        model = TestModel(image=image_data)
        assert isinstance(model.image, Base64Image)


def test_base64_image_error_in_models():
    class TestModel(BaseModel):
        image: Base64ImageInputType

    with pytest.raises(ValueError):
        TestModel(image='not a base64 image')
