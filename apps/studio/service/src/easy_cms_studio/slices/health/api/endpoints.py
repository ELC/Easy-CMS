from pathlib import Path
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from starlette.responses import PlainTextResponse

from easy_cms_studio.injections import Container
from easy_cms_studio.slices.health.application import HealthService

from .examples import HEALTH_PROBLEM_EXAMPLE, HEALTH_RESPONSE_EXAMPLE
from .schemas import HealthResponse, ProblemDetails

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": HEALTH_RESPONSE_EXAMPLE,
                },
            },
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ProblemDetails,
            "content": {
                "application/problem+json": {
                    "example": HEALTH_PROBLEM_EXAMPLE,
                },
            },
        },
    },
)
@inject
async def read_health(
    service: Annotated[HealthService, Depends(Provide[Container.health_service])],
) -> HealthResponse:
    return await service.read_health()


@router.get(
    "/problems/health-unavailable",
    include_in_schema=False,
    response_class=PlainTextResponse,
)
async def read_health_problem() -> PlainTextResponse:
    path = Path(__file__).parent.parent / "problems" / "health-unavailable.md"
    return PlainTextResponse(path.read_text(encoding="utf-8"), media_type="text/markdown")
