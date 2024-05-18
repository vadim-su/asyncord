import pytest
from pytest_mock import MockerFixture

from asyncord.client_hub import ClientHub


async def test_setup_single_client_group(mocker: MockerFixture) -> None:
    """Test setup_single_client_group method."""
    mock_client_group = mocker.patch('asyncord.client_hub.ClientGroup', autospec=True)
    async with ClientHub.setup_single_client_group('token') as client_group:
        assert client_group is mock_client_group.return_value


async def test_create_client_group(mocker: MockerFixture) -> None:  # noqa: RUF029
    """Test creation of a client group."""
    mock_client_group = mocker.patch('asyncord.client_hub.ClientGroup', autospec=True)
    hub = ClientHub()
    hub.create_client_group('group_name', 'token')

    mock_client_group.assert_called_once()

    with pytest.raises(ValueError, match=r'Client group group_name already exists'):
        hub.create_client_group('group_name', 'token')
