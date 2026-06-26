import pytest
from easy_cms_shared import HealthStatus, ServiceIdentity
from httpx import AsyncClient
from syrupy.assertion import SnapshotAssertion

from easy_cms_sync_server.slices.health.api.responses import HealthResponse


@pytest.fixture
def expected_health_response() -> HealthResponse:
    return HealthResponse(
        status=HealthStatus.HEALTHY,
        service=ServiceIdentity.SYNC_SERVER_SERVICE,
    )


async def test_read_health_returns_pydantic_payload(
    http_client: AsyncClient,
    expected_health_response: HealthResponse,
    snapshot: SnapshotAssertion,
) -> None:
    response = await http_client.get("/health")

    assert response.status_code == 200
    parsed_response = HealthResponse.model_validate_json(response.text)
    assert parsed_response == expected_health_response
    assert parsed_response.model_dump(mode="json") == snapshot


async def test_read_health_problem_returns_markdown_page(http_client: AsyncClient) -> None:
    response = await http_client.get("/problems/health-unavailable")

    assert response.status_code == 200
    assert "Problem type URI: `/problems/health-unavailable`" in response.text
