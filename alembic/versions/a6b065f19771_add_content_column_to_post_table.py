"""add content column to post table

Revision ID: a6b065f19771
Revises: fff29c4510df
Create Date: 2024-12-26 18:37:50.001182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6b065f19771'
down_revision: Union[str, None] = 'fff29c4510df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
