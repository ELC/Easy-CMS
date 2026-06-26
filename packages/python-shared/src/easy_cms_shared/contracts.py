from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "healthy",
                    "service": "sync-server-service",
                },
            ],
        },
    )

    status: str = Field(examples=["healthy"])
    service: str = Field(examples=["sync-server-service"])


class VersionResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "version": "0.1.0",
                    "service": "sync-server-service",
                },
            ],
        },
    )

    version: str = Field(examples=["0.1.0"])
    service: str = Field(examples=["sync-server-service"])


class ProblemDetails(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "type": "/problems/example-problem",
                    "title": "Example problem",
                    "status": 500,
                    "detail": "A support-facing explanation of the problem.",
                    "instance": "/requests/example",
                },
            ],
        },
    )

    type: str = Field(examples=["/problems/example-problem"])
    title: str = Field(examples=["Example problem"])
    status: int = Field(examples=[500])
    detail: str = Field(examples=["A support-facing explanation of the problem."])
    instance: str | None = Field(default=None, examples=["/requests/example"])
