from easy_cms_shared import HealthStatus, ServiceIdentity
from pydantic import BaseModel


class HealthReport(BaseModel):
    status: HealthStatus
    service: ServiceIdentity
