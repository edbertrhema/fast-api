"""add last few column in products table

Revision ID: 1207d5ac0d86
Revises: 750a1fdc8d14
Create Date: 2023-09-21 20:10:33.064330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1207d5ac0d86'
down_revision: Union[str, None] = '750a1fdc8d14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('is_sale', sa.Boolean(),default=True))
    op.add_column('products', sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False))

    pass


def downgrade() -> None:
    op.drop_column('products','is_sale')
    op.drop_column('products','created_at')
    pass
