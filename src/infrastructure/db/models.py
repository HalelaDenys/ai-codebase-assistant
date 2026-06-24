from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import TIMESTAMP, func, MetaData, UUID, text, Enum
from core import settings
from datetime import datetime
import uuid
from entities.schemas import RepoStatusEnum


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=settings.db.naming_convention)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuidv7()"),
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Repositories(Base):
    __tablename__ = "repositories"

    repo_url: Mapped[str] = mapped_column(nullable=False)
    branch: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[RepoStatusEnum] = mapped_column(
        Enum(
            RepoStatusEnum,
            values_callable=lambda enum: [e.value for e in enum],
            name="status_enum_type",
        ),
        nullable=False,
        default=RepoStatusEnum.QUEUED,
        server_default=text(f"'{RepoStatusEnum.QUEUED.value}'"),
    )
    path_url: Mapped[str | None] = mapped_column(nullable=True)
    error_message: Mapped[str | None] = mapped_column(nullable=True)
