from importlib.metadata import PackageNotFoundError, version

from easy_cms_shared import VersionResponse

from easy_cms_sync_server.slices.version.domain import VersionUnavailable


class VersionService:
    def __init__(self, distribution_name: str, service_name: str) -> None:
        self._distribution_name = distribution_name
        self._service_name = service_name

    async def read_version(self) -> VersionResponse:
        try:
            package_version = version(self._distribution_name)
        except PackageNotFoundError as exc:
            raise VersionUnavailable from exc
        return VersionResponse(version=package_version, service=self._service_name)
