from __future__ import annotations

import pytest

from asyncord.client.applications.models.requests import (
    UpdateApplicationRequest,
)
from asyncord.client.applications.resources import ApplicationResource
from tests.conftest import IntegrationTestData


@pytest.mark.skip(reason='Dangerous operation. Needs manual control.')
async def test_update_application(
    applications_res: ApplicationResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test update application.

    This test is skipped by default because I have not enough friends to test this.
    """
    app = await applications_res.update_application(
        UpdateApplicationRequest(
            description='This is a test description.',
        ),
    )

    assert app.description == 'This is a test description.'


async def test_get_application(
    applications_res: ApplicationResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test get application."""
    app = await applications_res.get_application()

    assert app.id == integration_data.app_id


async def test_get_application_role_metadata(
    applications_res: ApplicationResource,
    integration_data: IntegrationTestData,
) -> None:
    """Test get application role connection metadata."""
    metadata_records = await applications_res.get_application_role_connection_metadata_records(
        integration_data.app_id,
    )

    assert isinstance(metadata_records, list)
