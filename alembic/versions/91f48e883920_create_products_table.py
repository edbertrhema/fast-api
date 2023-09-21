"""create products table

Revision ID: 91f48e883920
Revises: 
Create Date: 2023-09-21 19:41:32.185428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91f48e883920'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('products', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    , sa.Column('name', sa.String(255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('products')
    pass
