import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import main_router
from core import register_error_handlers, settings
from infrastructure import broker, db_helper

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("Starting Lifespan")
    await broker.start()
    yield

    await broker.stop()
    await db_helper.dispose()
    logging.info("Stopping Lifespan")


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    register_error_handlers(app)

    app.include_router(main_router)

    return app
