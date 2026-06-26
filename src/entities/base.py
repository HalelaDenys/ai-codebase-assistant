from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class BaseSchemas(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RepoStatusEnum(StrEnum):
    QUEUED = "queued"
    CLONING = "cloning"
    INDEXING = "indexing"
    READY = "ready"
    FAILED = "failed"
