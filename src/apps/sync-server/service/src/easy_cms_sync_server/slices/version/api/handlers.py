from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from ..domain import VersionUnavailable
from .responses import ProblemDetails


async def version_unavailable_handler(_request: Request, exc: Exception) -> JSONResponse:
    detail = exc.detail if isinstance(exc, VersionUnavailable) else "Sync Server version could not be reported."
    problem = ProblemDetails(
        type="/problems/version-unavailable",
        title="Version unavailable",
        status=500,
        detail=detail,
    )
    return JSONResponse(status_code=500, content=problem.model_dump())


exception_handlers: list[tuple[type[Exception], Callable[[Request, Exception], Awaitable[Response]]]] = [
    (VersionUnavailable, version_unavailable_handler),
]
