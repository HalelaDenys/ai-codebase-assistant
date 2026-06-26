from uuid import UUID

from sqlalchemy.exc import IntegrityError

from core.exceptions import AlreadyExistsError, NotFoundError
from entities.base import RepoStatusEnum
from entities.dto import CreateRepositoryDTO
from entities.schemas import CreateRepoResponseS, CreateRepositoryS
from infrastructure import Repositories, RepositoryRepo, RepositoryTaskPublisher


class RepositoryService:
    def __init__(
        self,
        repository_repo: RepositoryRepo,
        task_publisher: RepositoryTaskPublisher,
    ) -> Repositories:
        self._repo = repository_repo
        self._publisher = task_publisher

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
            await self._repo.commit()
        except IntegrityError as e:
            raise AlreadyExistsError(
                f"Repository '{repo_url}' with branch '{data.branch}' already exists"
            ) from e

        await self._publisher.publish_index_task(new_instance.id)

        return CreateRepoResponseS(repo_id=new_instance.id, status=new_instance.status)

    async def get(self, repo_id: UUID) -> Repositories:
        if not (repo := await self._repo.find_single(id=repo_id)):
            raise NotFoundError("Repository not found")
        return repo
