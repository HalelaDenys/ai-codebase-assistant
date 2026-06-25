from uuid import UUID

from sqlalchemy.exc import IntegrityError

from core.exeptions import AlreadyExistsError, NotFoundError
from entities.dto import CreateRepositoryDTO
from entities.schemas import CreateRepoResponseS, CreateRepositoryS, RepoStatusEnum
from infrastructure import Repositories, RepositoryRepo


class RepositoryService:
    def __init__(self, repository_repo: RepositoryRepo) -> Repositories:
        self._repo = repository_repo

    async def create(self, data: CreateRepositoryS) -> CreateRepoResponseS:
        repo_url = str(data.repo_url)
        if await self._repo.find_single(repo_url=repo_url, branch=data.branch):
            raise AlreadyExistsError(
                f"Repository '{repo_url}' with branch '{data.branch}' already exists"
            )

        payload = CreateRepositoryDTO(
            repo_url=repo_url,
            branch=data.branch,
            status=RepoStatusEnum.QUEUED,
        )

        try:
            new_instance = await self._repo.create(payload)
        except IntegrityError as e:
            raise AlreadyExistsError(
                f"Repository '{repo_url}' with branch '{data.branch}' already exists"
            ) from e
        return CreateRepoResponseS(repo_id=new_instance.id, status=new_instance.status)

    async def get(self, repo_id: UUID) -> Repositories:
        if not (repo := await self._repo.find_single(id=repo_id)):
            raise NotFoundError("Repository not found")
        return repo
