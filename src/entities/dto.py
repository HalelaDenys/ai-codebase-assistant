from pydantic import BaseModel

from entities.schemas import RepoStatusEnum


class CreateRepositoryDTO(BaseModel):
    repo_url: str
    branch: str
    status: RepoStatusEnum


class UpdateRepositoryDTO(BaseModel):
    status: RepoStatusEnum | None = None
    path_url: str | None = None
    error_message: str | None = None
