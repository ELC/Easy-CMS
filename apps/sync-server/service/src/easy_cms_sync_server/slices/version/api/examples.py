from typing import Final

VERSION_RESPONSE_EXAMPLE: Final = {
    "version": "0.1.0",
    "service": "sync-server-service",
}

VERSION_PROBLEM_EXAMPLE: Final = {
    "type": "/problems/version-unavailable",
    "title": "Version unavailable",
    "status": 500,
    "detail": "Sync Server version could not be reported.",
    "instance": None,
}
