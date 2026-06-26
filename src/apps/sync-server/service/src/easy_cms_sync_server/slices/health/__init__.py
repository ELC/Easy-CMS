from collections.abc import Callable

from fastapi import FastAPI

from .api.endpoints import router
from .api.handlers import exception_handlers
from .application import HealthService

MiddlewareRegistrar = Callable[[FastAPI], None]
routers = [router]
middleware: list[MiddlewareRegistrar] = []

__all__ = ["HealthService", "exception_handlers", "middleware", "routers"]
