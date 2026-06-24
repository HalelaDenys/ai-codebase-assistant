from pydantic import BaseModel, HttpUrl
from uuid import UUID
from enum import Enum


class RepoStatusEnum(str, Enum):
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
