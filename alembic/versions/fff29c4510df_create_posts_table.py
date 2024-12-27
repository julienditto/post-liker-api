"""create posts table

Revision ID: fff29c4510df
Revises: 
Create Date: 2024-12-26 18:28:51.394919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fff29c4510df'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
