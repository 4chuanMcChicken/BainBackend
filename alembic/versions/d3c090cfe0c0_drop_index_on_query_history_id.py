"""drop index on query_history.id

Revision ID: d3c090cfe0c0
Revises: 821ace9f7be5
Create Date: 2025-06-07 00:55:06.216357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3c090cfe0c0'
down_revision: Union[str, None] = '821ace9f7be5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_query_history_id'), table_name='query_history')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_query_history_id'), 'query_history', ['id'], unique=False)
    # ### end Alembic commands ###
