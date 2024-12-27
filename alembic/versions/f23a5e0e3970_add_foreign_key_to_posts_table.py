"""add foreign key to posts table

Revision ID: f23a5e0e3970
Revises: 8fb84131d1d8
Create Date: 2024-12-26 18:54:05.468275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f23a5e0e3970'
down_revision: Union[str, None] = '8fb84131d1d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', 
                          referent_table='users', local_cols=['owner_id'], 
                          remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
