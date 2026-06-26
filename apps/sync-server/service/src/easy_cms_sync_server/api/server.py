from uvicorn import Config, Server

from .app import app_factory


def server_factory() -> Server:
    config = Config(
        app=app_factory,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        factory=True,
    )
    return Server(config)
