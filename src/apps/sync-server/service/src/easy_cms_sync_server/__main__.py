import asyncio

import easy_cms_sync_server

from .api import app_factory, server_factory
from .injections import Container


async def main() -> None:
    container = Container()
    container.wire(packages=[easy_cms_sync_server])
    server = server_factory(app_factory())
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
