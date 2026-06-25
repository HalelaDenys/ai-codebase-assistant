import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import main_router
from core import settings
from infrastructure import db_helper

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("Starting Lifespan")
    yield

    await db_helper.dispose()
    logging.info("Stopping Lifespan")


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(main_router)

    return app
