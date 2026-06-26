from pathlib import Path
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.responses import PlainTextResponse

from ..application import VersionService
from .examples import VERSION_ROUTE_RESPONSES
from .responses import VersionResponse

router = APIRouter(tags=["version"])


@router.get(
    "/version",
    responses=VERSION_ROUTE_RESPONSES,
)
@inject
async def read_version(
    service: Annotated[VersionService, Depends(Provide["version_service"])],
) -> VersionResponse:
    report = await service.read_version()
    return VersionResponse(version=report.version, service=report.service)


@router.get(
    "/problems/version-unavailable",
    include_in_schema=False,
    response_class=PlainTextResponse,
)
async def read_version_problem() -> PlainTextResponse:
    path = Path(__file__).parent.parent / "problems" / "version-unavailable.md"
    return PlainTextResponse(path.read_text(encoding="utf-8"), media_type="text/markdown")
