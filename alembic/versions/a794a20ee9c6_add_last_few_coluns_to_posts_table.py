"""add last few coluns to posts table

Revision ID: a794a20ee9c6
Revises: f23a5e0e3970
Create Date: 2024-12-26 19:14:10.170704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a794a20ee9c6'
down_revision: Union[str, None] = 'f23a5e0e3970'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column(
        "published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column(
        "created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
