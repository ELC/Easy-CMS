from easy_cms_shared import HealthResponse


class HealthService:
    def __init__(self, service_name: str) -> None:
        self._service_name = service_name

    async def read_health(self) -> HealthResponse:
        return HealthResponse(status="healthy", service=self._service_name)
