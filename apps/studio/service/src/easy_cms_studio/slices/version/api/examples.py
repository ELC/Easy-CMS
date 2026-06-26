from typing import Final

VERSION_RESPONSE_EXAMPLE: Final = {
    "version": "0.1.0",
    "service": "studio-service",
}

VERSION_PROBLEM_EXAMPLE: Final = {
    "type": "/problems/version-unavailable",
    "title": "Version unavailable",
    "status": 500,
    "detail": "CMS Studio sidecar version could not be reported.",
    "instance": None,
}
