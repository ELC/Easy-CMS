from importlib.metadata import PackageNotFoundError, version

from easy_cms_shared import ServiceIdentity
from pydantic import BaseModel

from ..domain import VersionReport, VersionUnavailable


class VersionService(BaseModel):
    distribution_name: str
    service: ServiceIdentity

    async def read_version(self) -> VersionReport:
        try:
            package_version = version(self.distribution_name)
        except PackageNotFoundError as exc:
            raise VersionUnavailable from exc
        return VersionReport(version=package_version, service=self.service)
