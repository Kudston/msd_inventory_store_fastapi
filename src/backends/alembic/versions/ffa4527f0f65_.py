"""empty message

Revision ID: ffa4527f0f65
Revises: 1cd579432217
Create Date: 2024-07-30 01:42:25.530730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffa4527f0f65'
down_revision: Union[str, None] = '1cd579432217'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('date_modified', sa.DateTime(), nullable=True))
    op.alter_column('products', 'price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.drop_column('orders', 'date_modified')
    # ### end Alembic commands ###
