"""add column to products table

Revision ID: b817a342ab54
Revises: 91f48e883920
Create Date: 2023-09-21 19:51:57.206691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b817a342ab54'
down_revision: Union[str, None] = '91f48e883920'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('price', sa.Integer(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('products','price')
    pass
