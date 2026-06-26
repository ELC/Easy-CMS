from easy_cms_shared import ServiceIdentity
from pydantic import BaseModel


class VersionReport(BaseModel):
    version: str
    service: ServiceIdentity
