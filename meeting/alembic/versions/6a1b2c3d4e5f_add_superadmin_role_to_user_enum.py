"""add_superadmin_role_to_user_enum

Revision ID: 6a1b2c3d4e5f
Revises: ffa7f9c8af57
Create Date: 2026-06-13 09:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '6a1b2c3d4e5f'
down_revision: Union[str, Sequence[str], None] = 'ffa7f9c8af57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

old_enum = ("Admin", "User", "Host")
new_enum = ("Admin", "User", "Host", "SuperAdmin")

enum_name = "role"


def upgrade() -> None:
    op.execute(f"ALTER TYPE {enum_name} RENAME TO {enum_name}_old")

    op.execute(f"CREATE TYPE {enum_name} AS ENUM('{new_enum[0]}', '{new_enum[1]}', '{new_enum[2]}', '{new_enum[3]}')")

    op.execute(
        f"ALTER TABLE users ALTER COLUMN role TYPE {enum_name} USING "
        f"(CASE "
        f"  WHEN role::text = 'Admin' THEN 'Admin'::{enum_name} "
        f"  WHEN role::text = 'Host' THEN 'Host'::{enum_name} "
        f"  WHEN role::text = 'User' THEN 'User'::{enum_name} "
        f"  ELSE 'User'::{enum_name} "
        f"END)"
    )

    op.execute(f"DROP TYPE {enum_name}_old")


def downgrade() -> None:
    op.execute(f"ALTER TYPE {enum_name} RENAME TO {enum_name}_new")
    op.execute(f"CREATE TYPE {enum_name} AS ENUM('{old_enum[0]}', '{old_enum[1]}', '{old_enum[2]}')")

    op.execute(
        f"ALTER TABLE users ALTER COLUMN role TYPE {enum_name} USING "
        f"(CASE "
        f"  WHEN role::text = 'Admin' THEN 'Admin'::{enum_name} "
        f"  WHEN role::text = 'Host' THEN 'Host'::{enum_name} "
        f"  WHEN role::text = 'User' THEN 'User'::{enum_name} "
        f"  WHEN role::text = 'SuperAdmin' THEN 'Admin'::{enum_name} "
        f"  ELSE 'User'::{enum_name} "
        f"END)"
    )

    op.execute(f"DROP TYPE {enum_name}_new")
