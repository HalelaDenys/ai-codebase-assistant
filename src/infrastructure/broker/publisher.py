from uuid import UUID

from faststream.rabbit import RabbitBroker

from core import settings
from entities.dto import IndexRepositoryMessage


class RepositoryTaskPublisher:
    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def publish_index_task(self, repo_id: UUID):
        message = IndexRepositoryMessage(repo_id=repo_id)
        await self._broker.publish(
            message.model_dump(mode="json"),
            queue=settings.rag.index_queue,
            persist=True,
            message_id=str(repo_id),
        )
