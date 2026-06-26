import json
from pathlib import Path

import pytest
from easy_cms_shared import ServiceIdentity
from fastapi import FastAPI
from starlette.requests import Request

from easy_cms_studio.api.app import app_factory
from easy_cms_studio.api.openapi import main as write_openapi
from easy_cms_studio.api.server import server_factory
from easy_cms_studio.slices.health.api.handlers import health_unavailable_handler
from easy_cms_studio.slices.health.api.responses import ProblemDetails as HealthProblemDetails
from easy_cms_studio.slices.health.domain import HealthUnavailable
from easy_cms_studio.slices.version.api.handlers import version_unavailable_handler
from easy_cms_studio.slices.version.api.responses import ProblemDetails as VersionProblemDetails
from easy_cms_studio.slices.version.application import VersionService
from easy_cms_studio.slices.version.domain import VersionUnavailable


def test_app_factory_creates_app() -> None:
    app = app_factory()

    assert app.title == "CMS Studio sidecar"


def test_server_factory_uses_supplied_app(app: FastAPI) -> None:
    server = server_factory(app)

    assert server.config.app is app
    assert server.config.port == 8001


def test_openapi_writer_creates_checked_in_schema() -> None:
    write_openapi()
    schema_path = Path(__file__).parents[3] / "openapi.json"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    assert schema["info"]["title"] == "CMS Studio sidecar"


async def test_health_unavailable_handler_returns_problem_details() -> None:
    request = Request({"type": "http", "method": "GET", "path": "/health", "headers": []})

    response = await health_unavailable_handler(request, HealthUnavailable("Dependency failed."))
    parsed_response = HealthProblemDetails.model_validate_json(bytes(response.body).decode())

    assert response.status_code == 503
    assert parsed_response.detail == "Dependency failed."


async def test_version_unavailable_handler_returns_problem_details() -> None:
    request = Request({"type": "http", "method": "GET", "path": "/version", "headers": []})

    response = await version_unavailable_handler(request, VersionUnavailable("Package metadata missing."))
    parsed_response = VersionProblemDetails.model_validate_json(bytes(response.body).decode())

    assert response.status_code == 500
    assert parsed_response.detail == "Package metadata missing."


async def test_version_service_raises_domain_exception_for_missing_distribution() -> None:
    service = VersionService(
        distribution_name="missing-easy-cms-distribution",
        service=ServiceIdentity.STUDIO_SERVICE,
    )

    with pytest.raises(VersionUnavailable, match=r"CMS Studio sidecar version could not be reported\."):
        await service.read_version()
