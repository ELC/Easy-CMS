import asyncio

import easy_cms_studio

from .api import app_factory, server_factory
from .injections import Container


async def main() -> None:
    container = Container()
    container.wire(packages=[easy_cms_studio])
    server = server_factory(app_factory())
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
