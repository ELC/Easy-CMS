from httpx import AsyncClient


async def test_read_health_returns_pydantic_payload(http_client: AsyncClient) -> None:
    response = await http_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "studio-service",
    }


async def test_read_health_problem_returns_markdown_page(http_client: AsyncClient) -> None:
    response = await http_client.get("/problems/health-unavailable")

    assert response.status_code == 200
    assert "Problem type URI: `/problems/health-unavailable`" in response.text
