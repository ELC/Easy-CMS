from httpx import AsyncClient


async def test_read_version_returns_installed_package_version(http_client: AsyncClient) -> None:
    response = await http_client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "version": "0.1.0",
        "service": "studio-service",
    }


async def test_read_version_problem_returns_markdown_page(http_client: AsyncClient) -> None:
    response = await http_client.get("/problems/version-unavailable")

    assert response.status_code == 200
    assert "Problem type URI: `/problems/version-unavailable`" in response.text
