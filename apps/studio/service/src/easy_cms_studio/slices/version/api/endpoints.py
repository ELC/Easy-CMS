from pathlib import Path
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from starlette.responses import PlainTextResponse

from easy_cms_studio.injections import Container
from easy_cms_studio.slices.version.application import VersionService

from .examples import VERSION_PROBLEM_EXAMPLE, VERSION_RESPONSE_EXAMPLE
from .schemas import ProblemDetails, VersionResponse

router = APIRouter(tags=["version"])


@router.get(
    "/version",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": VERSION_RESPONSE_EXAMPLE,
                },
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ProblemDetails,
            "content": {
                "application/problem+json": {
                    "example": VERSION_PROBLEM_EXAMPLE,
                },
            },
        },
    },
)
@inject
async def read_version(
    service: Annotated[VersionService, Depends(Provide[Container.version_service])],
) -> VersionResponse:
    return await service.read_version()


@router.get(
    "/problems/version-unavailable",
    include_in_schema=False,
    response_class=PlainTextResponse,
)
async def read_version_problem() -> PlainTextResponse:
    path = Path(__file__).parent.parent / "problems" / "version-unavailable.md"
    return PlainTextResponse(path.read_text(encoding="utf-8"), media_type="text/markdown")
