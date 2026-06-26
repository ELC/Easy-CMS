from dependency_injector import containers, providers
from easy_cms_shared import ServiceIdentity

from ..slices.health import HealthService
from ..slices.version import VersionService


class Container(containers.DeclarativeContainer):
    health_service = providers.Factory(
        HealthService,
        service=ServiceIdentity.STUDIO_SERVICE,
    )
    version_service = providers.Factory(
        VersionService,
        distribution_name="studio-service",
        service=ServiceIdentity.STUDIO_SERVICE,
    )
