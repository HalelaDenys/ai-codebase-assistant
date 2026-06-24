"""Init table Repositories

Revision ID: 882e149d2d93
Revises:
Create Date: 2026-06-24 12:41:38.137170

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "882e149d2d93"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "repositories",
        sa.Column("id", sa.UUID(), server_default=sa.text("uuidv7()"), nullable=False),
        sa.Column("repo_url", sa.String(), nullable=False),
        sa.Column("branch", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "queued",
                "cloning",
                "indexing",
                "ready",
                "failed",
                name="status_enum_type",
            ),
            server_default=sa.text("'queued'"),
            nullable=False,
        ),
        sa.Column("path_url", sa.String(), nullable=True),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_repositories")),
    )


def downgrade() -> None:
    op.drop_table("repositories")
