from collections.abc import Awaitable, Callable

from fastapi import APIRouter, FastAPI
from starlette.requests import Request
from starlette.responses import Response

from .health import exception_handlers as health_exception_handlers
from .health import middleware as health_middleware
from .health import routers as health_routers
from .version import exception_handlers as version_exception_handlers
from .version import middleware as version_middleware
from .version import routers as version_routers

ExceptionHandler = Callable[[Request, Exception], Awaitable[Response]]
MiddlewareRegistrar = Callable[[FastAPI], None]

routers: list[APIRouter] = [*health_routers, *version_routers]
exception_handlers: list[tuple[type[Exception], ExceptionHandler]] = [
    *health_exception_handlers,
    *version_exception_handlers,
]
middleware: list[MiddlewareRegistrar] = [*health_middleware, *version_middleware]

__all__ = ["exception_handlers", "middleware", "routers"]
