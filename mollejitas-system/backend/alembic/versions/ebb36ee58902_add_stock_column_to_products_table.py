"""add stock column to products table

Revision ID: ebb36ee58902
Revises: a80ec6d81f24
Create Date: 2025-07-03 16:13:16.164438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebb36ee58902'
down_revision: Union[str, Sequence[str], None] = 'a80ec6d81f24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('productos', sa.Column('stock', sa.Integer(), nullable=False, server_default='0'))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('productos', 'stock')
    # ### end Alembic commands ###
