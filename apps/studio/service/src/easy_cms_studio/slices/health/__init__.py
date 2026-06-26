from collections.abc import Callable

from fastapi import FastAPI

from .api.endpoints import router
from .api.handlers import exception_handlers

routers = [router]
middleware: list[Callable[[FastAPI], None]] = []

__all__ = ["exception_handlers", "middleware", "routers"]
