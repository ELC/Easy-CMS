from pathlib import Path
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.responses import PlainTextResponse

from ..application import HealthService
from .examples import HEALTH_ROUTE_RESPONSES
from .responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    responses=HEALTH_ROUTE_RESPONSES,
)
@inject
async def read_health(
    service: Annotated[HealthService, Depends(Provide["health_service"])],
) -> HealthResponse:
    report = await service.read_health()
    return HealthResponse(status=report.status, service=report.service)


@router.get(
    "/problems/health-unavailable",
    include_in_schema=False,
    response_class=PlainTextResponse,
)
async def read_health_problem() -> PlainTextResponse:
    path = Path(__file__).parent.parent / "problems" / "health-unavailable.md"
    return PlainTextResponse(path.read_text(encoding="utf-8"), media_type="text/markdown")
