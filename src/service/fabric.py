from collections.abc import AsyncGenerator

from infrastructure import RepositoryRepo, db_helper
from service.repo_service import RepositoryService


async def get_repo_service() -> AsyncGenerator[RepositoryService, None]:
    async with db_helper.get_session() as session:
        repo = RepositoryRepo(session=session)
        yield RepositoryService(repository_repo=repo)
