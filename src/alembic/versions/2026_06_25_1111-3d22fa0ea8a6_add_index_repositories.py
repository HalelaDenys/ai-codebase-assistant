"""add index Repositories

Revision ID: 3d22fa0ea8a6
Revises: 882e149d2d93
Create Date: 2026-06-25 11:11:48.224745

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d22fa0ea8a6"
down_revision: str | Sequence[str] | None = "882e149d2d93"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        op.f("uq_repositories_repo_url_branch"), "repositories", ["repo_url", "branch"]
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("uq_repositories_repo_url_branch"), "repositories", type_="unique"
    )
