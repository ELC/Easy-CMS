from easy_cms_shared import HealthStatus, ServiceIdentity
from pydantic import BaseModel

from ..domain import HealthReport


class HealthService(BaseModel):
    service: ServiceIdentity

    async def read_health(self) -> HealthReport:
        return HealthReport(status=HealthStatus.HEALTHY, service=self.service)
