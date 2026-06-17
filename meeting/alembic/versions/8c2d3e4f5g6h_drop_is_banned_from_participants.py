"""drop_is_banned_from_participants

Revision ID: 8c2d3e4f5g6h
Revises: 7b1c2d3e4f5g
Create Date: 2026-06-17 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '8c2d3e4f5g6h'
down_revision: Union[str, Sequence[str], None] = '7b1c2d3e4f5g'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('meet_participants', 'is_banned')


def downgrade() -> None:
    op.add_column(
        'meet_participants',
        sa.Column('is_banned', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    )
