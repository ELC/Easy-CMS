from fastapi import FastAPI

from ..slices import exception_handlers, middleware, routers


def app_factory() -> FastAPI:
    app = FastAPI(
        title="CMS Studio sidecar",
        version="0.1.0",
    )

    for register_middleware in middleware:  # pragma: no cover
        register_middleware(app)

    for exception_type, handler in exception_handlers:
        app.add_exception_handler(exception_type, handler)

    for router in routers:
        app.include_router(router)

    return app
