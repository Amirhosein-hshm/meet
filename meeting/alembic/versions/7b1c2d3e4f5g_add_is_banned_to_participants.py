"""add_is_banned_to_participants

Revision ID: 7b1c2d3e4f5g
Revises: 6a1b2c3d4e5f
Create Date: 2026-06-14 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7b1c2d3e4f5g'
down_revision: Union[str, Sequence[str], None] = '6a1b2c3d4e5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'meet_participants',
        sa.Column('is_banned', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    )


def downgrade() -> None:
    op.drop_column('meet_participants', 'is_banned')
