from fastapi import FastAPI

from easy_cms_studio.injections import Container
from easy_cms_studio.slices.health import exception_handlers as health_exception_handlers
from easy_cms_studio.slices.health import middleware as health_middleware
from easy_cms_studio.slices.health import routers as health_routers
from easy_cms_studio.slices.health.api import endpoints as health_endpoints
from easy_cms_studio.slices.version import exception_handlers as version_exception_handlers
from easy_cms_studio.slices.version import middleware as version_middleware
from easy_cms_studio.slices.version import routers as version_routers
from easy_cms_studio.slices.version.api import endpoints as version_endpoints


def app_factory(container: Container | None = None) -> FastAPI:
    active_container = container or Container()
    active_container.wire(modules=[health_endpoints, version_endpoints])

    app = FastAPI(
        title="CMS Studio sidecar",
        version="0.1.0",
    )

    for register_middleware in [*health_middleware, *version_middleware]:  # pragma: no cover
        register_middleware(app)

    for exception_type, handler in [*health_exception_handlers, *version_exception_handlers]:
        app.add_exception_handler(exception_type, handler)

    for router in [*health_routers, *version_routers]:
        app.include_router(router)

    return app
