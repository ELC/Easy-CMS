from easy_cms_shared import ServiceIdentity
from pydantic import BaseModel


class VersionResponse(BaseModel):
    version: str
    service: ServiceIdentity


class ProblemDetails(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str | None = None
