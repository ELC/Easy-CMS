from fastapi import FastAPI
from uvicorn import Config, Server


def server_factory(app: FastAPI) -> Server:
    config = Config(
        app=app,
        host="127.0.0.1",
        port=8001,
        log_level="info",
    )
    return Server(config)
