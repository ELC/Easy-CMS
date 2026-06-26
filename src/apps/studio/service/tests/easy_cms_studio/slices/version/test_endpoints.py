import pytest
from easy_cms_shared import ServiceIdentity
from httpx import AsyncClient
from syrupy.assertion import SnapshotAssertion

from easy_cms_studio.slices.version.api.responses import VersionResponse


@pytest.fixture
def expected_version_response() -> VersionResponse:
    return VersionResponse(
        version="0.1.0",
        service=ServiceIdentity.STUDIO_SERVICE,
    )


async def test_read_version_returns_installed_package_version(
    http_client: AsyncClient,
    expected_version_response: VersionResponse,
    snapshot: SnapshotAssertion,
) -> None:
    response = await http_client.get("/version")

    assert response.status_code == 200
    parsed_response = VersionResponse.model_validate_json(response.text)
    assert parsed_response == expected_version_response
    assert parsed_response.model_dump(mode="json") == snapshot


async def test_read_version_problem_returns_markdown_page(http_client: AsyncClient) -> None:
    response = await http_client.get("/problems/version-unavailable")

    assert response.status_code == 200
    assert "Problem type URI: `/problems/version-unavailable`" in response.text
