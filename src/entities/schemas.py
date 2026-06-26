from uuid import UUID

from pydantic import HttpUrl

from entities.base import BaseSchemas


class CreateRepositoryS(BaseSchemas):
    repo_url: HttpUrl
    branch: str = "main"


class AskRequestS(BaseSchemas):
    question: str


class CreateRepoResponseS(BaseSchemas):
    repo_id: UUID
    status: str  # queued | cloning | indexing | ready | failed
