"""add default to todos timestamps

Revision ID: 8961b12e1386
Revises: 552d64b66cf6
Create Date: 2026-03-04 15:53:03.992294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8961b12e1386'
down_revision: Union[str, Sequence[str], None] = '552d64b66cf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "todos",
        "created_at",
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    op.alter_column(
        "todos",
        "updated_at",
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )


def downgrade():
    op.alter_column("todos", "created_at", server_default=None)
    op.alter_column("todos", "updated_at", server_default=None)
