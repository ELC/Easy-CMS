from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector import containers, providers

if TYPE_CHECKING:
    from easy_cms_studio.slices.health.application.services import HealthService
    from easy_cms_studio.slices.version.application.services import VersionService


def health_service_factory() -> HealthService:
    from easy_cms_studio.slices.health.application.services import HealthService

    return HealthService(service_name="studio-service")


def version_service_factory() -> VersionService:
    from easy_cms_studio.slices.version.application.services import VersionService

    return VersionService(
        distribution_name="studio-service",
        service_name="studio-service",
    )


class Container(containers.DeclarativeContainer):
    health_service = providers.Factory(health_service_factory)
    version_service = providers.Factory(version_service_factory)
