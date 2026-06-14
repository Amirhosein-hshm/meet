"""update_user_role_enum

Revision ID: ffa7f9c8af57
Revises: 04d41407227e
Create Date: 2026-06-07 08:45:42.265502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

enum_name = "role"

# revision identifiers, used by Alembic.
revision: str = 'ffa7f9c8af57'
down_revision: Union[str, Sequence[str], None] = '04d41407227e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(f"ALTER TYPE {enum_name} RENAME TO {enum_name}_old")
    
    op.execute(f"CREATE TYPE {enum_name} AS ENUM('Admin', 'User', 'Host')")
    
    op.execute(
        f"ALTER TABLE users ALTER COLUMN role TYPE {enum_name} USING "
        f"(CASE "
        f"  WHEN role::text = 'Admin' THEN 'Admin'::{enum_name} "
        f"  WHEN role::text = 'Customer' THEN 'User'::{enum_name} "
        f"  WHEN role::text = 'Freelancer' THEN 'User'::{enum_name} "
        f"  WHEN role::text = 'Supervisor' THEN 'Host'::{enum_name} "
        f"  ELSE 'User'::{enum_name} "  
        f"END)"
    )
    
    op.execute(f"DROP TYPE {enum_name}_old")


def downgrade() -> None:
    op.execute(f"ALTER TYPE {enum_name} RENAME TO {enum_name}_new")
    op.execute(f"CREATE TYPE {enum_name} AS ENUM('Admin', 'Customer', 'Freelancer', 'Supervisor')")
    
    op.execute(
        f"ALTER TABLE users ALTER COLUMN role TYPE {enum_name} USING "
        f"(CASE "
        f"  WHEN role::text = 'Admin' THEN 'Admin'::{enum_name} "
        f"  WHEN role::text = 'User' THEN 'Customer'::{enum_name} "
        f"  WHEN role::text = 'Host' THEN 'Supervisor'::{enum_name} "
        f"  ELSE 'Customer'::{enum_name} "
        f"END)"
    )
    
    op.execute(f"DROP TYPE {enum_name}_new")
