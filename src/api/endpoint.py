from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from core import settings
from entities.schemas import CreateRepoResponseS, CreateRepositoryS
from service.fabric import get_repo_service
from service.repo_service import RepositoryService

router = APIRouter(prefix=settings.api_prefix.repo)


@router.post(
    "",
    status_code=202,
    responses={
        202: {"description": "Success"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Server Error"},
    },
)
async def create_repository(
    payload: CreateRepositoryS,
    service: Annotated["RepositoryService", Depends(get_repo_service)],
) -> CreateRepoResponseS:
    return await service.create(data=payload)


@router.get(
    "{repo_id}/status",
    status_code=200,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
async def repository_status(repo_id: UUID) -> dict:
    return {"repo_id": repo_id, "status": "queued"}


@router.get(
    "/{repo_id}/ask",
    status_code=200,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)
async def ask(repo_id: UUID) -> dict:
    return {"repo_id": repo_id, "status": "queued"}
