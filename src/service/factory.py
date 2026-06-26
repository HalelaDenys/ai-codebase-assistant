from collections.abc import AsyncGenerator

from infrastructure import RepositoryRepo, RepositoryTaskPublisher, broker, db_helper
from service.repo_service import RepositoryService


async def get_repo_service() -> AsyncGenerator[RepositoryService, None]:
    async with db_helper.get_session() as session:
        repo = RepositoryRepo(session=session)
        publisher = RepositoryTaskPublisher(broker=broker)
        yield RepositoryService(repository_repo=repo, task_publisher=publisher)
