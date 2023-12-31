
import pytest
from pydantic import BaseModel

from asyncord.color import RGB, Color, ColorInput

DECIMAL_VALUE = 11189196


@pytest.fixture
def color() -> Color:
    return Color(0xaabbcc)


def test_create_color_from_constructor(color):
    assert color.value == DECIMAL_VALUE


@pytest.mark.parametrize(
    'color_value',
    [
        11189196,
        0xaabbcc,
        'aabbcc',
        '0xaabbcc',
        '#aabbcc',
        (170, 187, 204),
        RGB(170, 187, 204),
    ],
    ids=[
        'int',
        'hex int',
        'hex str',
        '0x prefix hex str',
        'web hex str',
        'rgb tuple',
        'RGB class',
    ],
)
def test_create_color(color_value: int | str | RGB | tuple[int, int, int]):
    color = Color.build(color_value)
    assert color.value == DECIMAL_VALUE


def test_compare_colors(color: Color):
    assert color == Color(DECIMAL_VALUE)
    assert color != Color(0x000000)
    assert color != DECIMAL_VALUE


def test_color_to_int(color: Color):
    assert int(color) == DECIMAL_VALUE


def test_color_to_str(color: Color):
    assert color.to_hex() == '0xaabbcc'


def test_color_to_rgb(color: Color):
    assert color.to_rgb() == RGB(170, 187, 204)


@pytest.mark.parametrize(
    'color_value',
    [
        11189196,
        0xaabbcc,
        'aabbcc',
        '0xaabbcc',
        '#aabbcc',
        (170, 187, 204),
        RGB(170, 187, 204),
    ],
    ids=[
        'int',
        'hex int',
        'hex str',
        '0x prefix hex str',
        'web hex str',
        'rgb tuple',
        'RGB class',
    ],
)
def test_color_in_models(color_value: int | str | RGB | tuple[int, int, int], color: Color):
    class TestModel(BaseModel):
        color: ColorInput

    model = TestModel(color=color_value)
    assert isinstance(model.color, Color)
    assert model.color == color

    assert model.model_dump() == {'color': color}
    assert model.model_dump(mode='json') == {'color': DECIMAL_VALUE}


def test_color_error_in_models():
    class TestModel(BaseModel):
        color: ColorInput

    with pytest.raises(ValueError):
        TestModel(color='not a color')


# @pytest.mark.parametrize('img_name', [Path(f'tests/data/{file_name}') for file_name in TEST_FILE_NAMES])
# def test_base64_images_in_models(img_name: Path):
#     class TestModel(BaseModel):
#         image: Base64ImageInput

#     with open(img_name, 'rb') as file:
#         image_data = file.read()
#         model = TestModel(image=image_data)
#         assert isinstance(model.image, Base64Image)


# def test_base64_image_error_in_models():
#     class TestModel(BaseModel):
#         image: Base64ImageInput

#     with pytest.raises(ValueError):
#         TestModel(image='not a base64 image')
