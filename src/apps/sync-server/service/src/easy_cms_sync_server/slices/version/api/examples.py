from typing import Any, Final

from easy_cms_shared import ServiceIdentity

from .responses import ProblemDetails, VersionResponse

VERSION_RESPONSE_EXAMPLE: Final = VersionResponse(
    version="0.1.0",
    service=ServiceIdentity.SYNC_SERVER_SERVICE,
).model_dump()

VERSION_PROBLEM_EXAMPLE: Final = ProblemDetails(
    type="/problems/version-unavailable",
    title="Version unavailable",
    status=500,
    detail="Sync Server version could not be reported.",
    instance=None,
).model_dump()

VERSION_ROUTE_RESPONSES: Final[dict[int | str, dict[str, Any]]] = {
    200: {
        "content": {
            "application/json": {
                "example": VERSION_RESPONSE_EXAMPLE,
            },
        },
    },
    500: {
        "model": ProblemDetails,
        "content": {
            "application/problem+json": {
                "example": VERSION_PROBLEM_EXAMPLE,
            },
        },
    },
}
