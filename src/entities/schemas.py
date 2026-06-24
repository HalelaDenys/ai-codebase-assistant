from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class RepoStatusEnum(StrEnum):
    QUEUED = "queued"
    CLONING = "cloning"
    INDEXING = "indexing"
    READY = "ready"
    FAILED = "failed"


class CreateRepositoryS(BaseModel):
    repo_url: HttpUrl
    branch: str = "main"


class AskRequestS(BaseModel):
    question: str


class CreateRepoResponseS(BaseModel):
    repo_id: UUID
    status: str  # queued | cloning | indexing | ready | failed
