import logging
from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPOS_DIR = Path("src/data/repos")
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class APIPrefix(BaseModel):
    api_v1: str = "/api/v1"
    repo: str = "/repositories"


class MiddlewareConfig(BaseModel):
    cors_allowed_origins: list[str] = [
        "http://localhost",
        "http://localhost:5173",
    ]


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"

    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class SQLAlchemyConfig(BaseSettings):
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 10


class DataBaseConfig(BaseSettings):
    naming_convention: ClassVar[dict] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    user: str
    password: str
    host: str
    port: int
    db: str
    alchemy_config: SQLAlchemyConfig = SQLAlchemyConfig()

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.db}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )

    midd: MiddlewareConfig
    db: DataBaseConfig
    api_prefix: APIPrefix = APIPrefix()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
