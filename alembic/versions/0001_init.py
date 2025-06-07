"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-02-14 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'query_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('destination', sa.String(), nullable=False),
        sa.Column('kilometers', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('miles', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_query_history_id'), 'query_history', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_query_history_id'), table_name='query_history')
    op.drop_table('query_history') 