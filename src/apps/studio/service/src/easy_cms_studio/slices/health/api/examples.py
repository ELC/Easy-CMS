from typing import Any, Final

from easy_cms_shared import HealthStatus, ServiceIdentity

from .responses import HealthResponse, ProblemDetails

HEALTH_RESPONSE_EXAMPLE: Final = HealthResponse(
    status=HealthStatus.HEALTHY,
    service=ServiceIdentity.STUDIO_SERVICE,
).model_dump()

HEALTH_PROBLEM_EXAMPLE: Final = ProblemDetails(
    type="/problems/health-unavailable",
    title="Health unavailable",
    status=503,
    detail="CMS Studio sidecar health could not be reported.",
    instance=None,
).model_dump()

HEALTH_ROUTE_RESPONSES: Final[dict[int | str, dict[str, Any]]] = {
    200: {
        "content": {
            "application/json": {
                "example": HEALTH_RESPONSE_EXAMPLE,
            },
        },
    },
    503: {
        "model": ProblemDetails,
        "content": {
            "application/problem+json": {
                "example": HEALTH_PROBLEM_EXAMPLE,
            },
        },
    },
}
