from fastapi import FastAPI


def test_openapi_includes_response_examples(app: FastAPI) -> None:
    schema = app.openapi()

    health_response = schema["paths"]["/health"]["get"]["responses"]["200"]
    version_response = schema["paths"]["/version"]["get"]["responses"]["200"]

    assert health_response["content"]["application/json"]["example"] == {
        "status": "healthy",
        "service": "studio-service",
    }
    assert version_response["content"]["application/json"]["example"] == {
        "version": "0.1.0",
        "service": "studio-service",
    }
