"""add foreign key to products table

Revision ID: 750a1fdc8d14
Revises: cb7b210f7c17
Create Date: 2023-09-21 20:04:43.961464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '750a1fdc8d14'
down_revision: Union[str, None] = 'cb7b210f7c17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('buyer_id', sa.Integer(), nullable=False))
    op.create_foreign_key('products_users_fk', source_table='products', referent_table='users',
    local_cols=['buyer_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('products_users_fk','products')
    op.drop_column('products','buyer_id')
    pass
