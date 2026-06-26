from easy_cms_shared import HealthStatus, ServiceIdentity


def test_health_status_values_are_stable() -> None:
    assert HealthStatus.HEALTHY == "healthy"


def test_service_identity_values_are_stable() -> None:
    assert ServiceIdentity.STUDIO_SERVICE == "studio-service"
    assert ServiceIdentity.SYNC_SERVER_SERVICE == "sync-server-service"
