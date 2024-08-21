from typing import Annotated

import pytest
from pydantic import AnyUrl, BaseModel
from yarl import URL

from asyncord.yarl_url import AttachmentUrl, HttpYarlUrl, YarlUrl, YarlUrlConstraint, YarlUrlType


class _TestModel[URL_TYPE: YarlUrl](BaseModel):
    """Model protocol."""

    url: URL_TYPE


@pytest.fixture(
    params=[
        YarlUrl,
        YarlUrlType,
        HttpYarlUrl,
        Annotated[YarlUrlType, YarlUrlConstraint(allowed_schemes=frozenset(('https', 'http')))],
    ],
)
def model_to_test(request: pytest.FixtureRequest) -> type[_TestModel]:
    """Model fixture."""
    url_type: type[YarlUrl] = request.param

    class TestModel(_TestModel[url_type]):
        pass

    return TestModel


def test_url_creation() -> None:
    """Test URL creation."""
    assert YarlUrl('https://example.com').raw_url == URL('https://example.com')


def test_url_validation() -> None:
    """Test URL validation."""
    test_url = URL('https://example.com')
    assert YarlUrl.validate('https://example.com').raw_url == test_url
    assert YarlUrl.validate(YarlUrl('https://example.com')).raw_url == test_url
    assert YarlUrl.validate(URL('https://example.com')).raw_url == test_url
    assert YarlUrl.validate(AnyUrl('https://example.com')).raw_url == test_url


def test_url_validation_failure() -> None:
    """Test URL validation failure."""
    with pytest.raises(ValueError, match='Invalid URL type:'):
        YarlUrl.validate(1)  # type: ignore


def test_url_in_model(model_to_test: type[_TestModel]) -> None:
    """Test URL in Pydantic model."""
    model = model_to_test(url='https://example.com')
    assert model.url == YarlUrl('https://example.com')
    assert model.url.raw_url == URL('https://example.com')  # type: ignore


def test_url_in_model_failure(model_to_test: type[_TestModel]) -> None:
    """Test URL in Pydantic model failure."""
    with pytest.raises(ValueError, match=r'.*validation errors for.*'):
        model_to_test(url=1)  # type: ignore


def test_url_json_dumps(model_to_test: type[_TestModel]) -> None:
    """Test URL JSON dumps."""
    model = model_to_test(url='https://example.com')

    dumped = model.model_dump_json()
    assert dumped == '{"url":"https://example.com"}'

    dumped = model.model_dump(mode='json')
    assert dumped == {'url': 'https://example.com'}


@pytest.mark.skip(reason='Pydantic has a bug or something that makes this test fail')
def test_url_dumps(model_to_test: type[_TestModel]) -> None:
    """Test URL dumps."""
    model = model_to_test(url='https://example.com')
    dumped = model.model_dump()
    assert dumped['url'] == URL('https://example.com')


@pytest.mark.parametrize(
    ('url_type', 'success_url', 'failure_url'),
    [
        (
            Annotated[YarlUrlType, YarlUrlConstraint(allowed_schemes=['https'])],
            'https://example.com',
            'http://example.com',
        ),
        (Annotated[YarlUrlType, YarlUrlConstraint(max_length=20)], 'https://example.com', 'https://example.com/long'),
        (HttpYarlUrl, 'https://example.com', 'some_schema://example.com'),
        (AttachmentUrl, 'attachment://example.com', 'https://example.com'),
    ],
)
def test_constraint(
    url_type: type[YarlUrlType],
    success_url: str,
    failure_url: str,
) -> None:
    """Test URL constraints."""

    class TestModel(BaseModel):
        url: url_type

    TestModel(url=success_url)
    with pytest.raises(ValueError, match=r'.*validation error for.*'):
        TestModel(url=failure_url)
