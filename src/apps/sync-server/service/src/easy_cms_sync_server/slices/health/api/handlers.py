from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from ..domain import HealthUnavailable
from .responses import ProblemDetails


async def health_unavailable_handler(_request: Request, exc: Exception) -> JSONResponse:
    detail = exc.detail if isinstance(exc, HealthUnavailable) else "Sync Server health could not be reported."
    problem = ProblemDetails(
        type="/problems/health-unavailable",
        title="Health unavailable",
        status=503,
        detail=detail,
    )
    return JSONResponse(status_code=503, content=problem.model_dump())


exception_handlers: list[tuple[type[Exception], Callable[[Request, Exception], Awaitable[Response]]]] = [
    (HealthUnavailable, health_unavailable_handler),
]
