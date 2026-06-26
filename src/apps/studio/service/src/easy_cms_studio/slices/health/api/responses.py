from easy_cms_shared import HealthStatus, ServiceIdentity
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: HealthStatus
    service: ServiceIdentity


class ProblemDetails(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str | None = None
