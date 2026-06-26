from collections.abc import Callable

from fastapi import FastAPI

from .api.endpoints import router
from .api.handlers import exception_handlers
from .application import VersionService

MiddlewareRegistrar = Callable[[FastAPI], None]
routers = [router]
middleware: list[MiddlewareRegistrar] = []

__all__ = ["VersionService", "exception_handlers", "middleware", "routers"]
