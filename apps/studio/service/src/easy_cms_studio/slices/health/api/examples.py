from typing import Final

HEALTH_RESPONSE_EXAMPLE: Final = {
    "status": "healthy",
    "service": "studio-service",
}

HEALTH_PROBLEM_EXAMPLE: Final = {
    "type": "/problems/health-unavailable",
    "title": "Health unavailable",
    "status": 503,
    "detail": "CMS Studio sidecar health could not be reported.",
    "instance": None,
}
