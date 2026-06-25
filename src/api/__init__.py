from fastapi import APIRouter

from api.endpoint import router
from core import settings

main_router = APIRouter(
    prefix=settings.api_prefix.api_v1,
    tags=["api"],
)

main_router.include_router(router)


@main_router.get("")
async def health() -> dict:
    return {"status": "ok"}
