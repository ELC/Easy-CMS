from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from easy_cms_sync_server.api import app_factory
from easy_cms_sync_server.injections import Container


@pytest.fixture
def test_container() -> Container:
    return Container()


@pytest.fixture(autouse=True)
def _install_test_container(test_container: Container) -> None:
    test_container.wire(packages=["easy_cms_sync_server"])


@pytest.fixture
def app(test_container: Container) -> FastAPI:
    return app_factory(test_container)


@pytest.fixture
async def http_client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
