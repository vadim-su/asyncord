from __future__ import annotations

from asyncord.client.applications.models.requests import (
    UpdateApplicationRequest,
)
from asyncord.client.applications.resources import ApplicationResource
from tests.conftest import IntegrationTestData


async def test_update_application(applications_res: ApplicationResource) -> None:
    """Test update application.

    This test is skipped by default because I have not enough friends to test this.
    """
    app = await applications_res.get_application()
    presaved_description = app.description
    presaved_tags = app.tags

    new_description = 'This is a test description'
    new_tags = {'test', 'tags'}
    app = await applications_res.update_application(
        UpdateApplicationRequest(
            description=new_description,
            tags=new_tags,
        ),
    )
    try:
        assert app.description == new_description
        assert app.tags == new_tags

    finally:
        # Reset the description
        app = await applications_res.update_application(
            UpdateApplicationRequest(
                description=presaved_description,
                tags=presaved_tags,
            ),
        )

    assert app.description == presaved_description
    assert app.tags == presaved_tags


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
