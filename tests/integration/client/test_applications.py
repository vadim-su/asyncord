from __future__ import annotations

import pytest

from asyncord.client.applications.resources import ApplicationResource
from asyncord.client.applications.models.requests import UpdateApplicationRequest
from asyncord.client.http.errors import ClientError
from tests.conftest import IntegrationTestData


@pytest.mark.skip(reason='Dangerous operation. Needs manual control.')
async def test_update_application(
    app_managment: ApplicationResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test update application.

    This test is skipped by default because I have not enough friends to test this.
    """
    app = await app_managment.update_application(
            UpdateApplicationRequest(
                description='This is a test description.',
            )
        )
    
    assert app.description == 'This is a test description.'




async def get_application(
    app_managment: ApplicationResource,
    integration_data: IntegrationTestData,
) -> None: 
    """Test get application."""
    app = await app_managment.get_application()

    assert app.id == integration_data.app_id