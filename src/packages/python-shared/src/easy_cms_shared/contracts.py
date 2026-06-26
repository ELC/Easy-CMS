from enum import StrEnum


class HealthStatus(StrEnum):
    HEALTHY = "healthy"


class ServiceIdentity(StrEnum):
    STUDIO_SERVICE = "studio-service"
    SYNC_SERVER_SERVICE = "sync-server-service"
