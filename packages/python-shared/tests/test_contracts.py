from easy_cms_shared import HealthResponse, ProblemDetails, VersionResponse


def test_health_response_serializes_service_status() -> None:
    response = HealthResponse(status="healthy", service="studio-service")

    assert response.model_dump() == {
        "status": "healthy",
        "service": "studio-service",
    }


def test_version_response_serializes_semantic_version() -> None:
    response = VersionResponse(version="0.1.0", service="sync-server-service")

    assert response.model_dump() == {
        "version": "0.1.0",
        "service": "sync-server-service",
    }


def test_problem_details_serializes_rfc_9457_fields() -> None:
    response = ProblemDetails(
        type="/problems/example-problem",
        title="Example problem",
        status=500,
        detail="A support-facing explanation of the problem.",
        instance="/requests/example",
    )

    assert response.model_dump() == {
        "type": "/problems/example-problem",
        "title": "Example problem",
        "status": 500,
        "detail": "A support-facing explanation of the problem.",
        "instance": "/requests/example",
    }
