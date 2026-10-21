"""Add the standard mechanical part groups and types for customer browsing.

Revision ID: 20261021_0008
Revises: 20261010_0007
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.orm import Session

from alembic import op
from app.part_types import PART_GROUPS, ensure_standard_part_types

revision: str = "20261021_0008"
down_revision: str | None = "20261010_0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    session = Session(bind=op.get_bind())
    ensure_standard_part_types(session)
    session.flush()


def downgrade() -> None:
    # Only types no product uses are removed, so catalog data is never orphaned.
    ids = [category.id for group in PART_GROUPS for category in group.types]
    ids += [group.id for group in PART_GROUPS]
    for category_id in ids:
        op.execute(
            sa.text(
                "DELETE FROM categories WHERE id = :id"
                " AND NOT EXISTS (SELECT 1 FROM products WHERE category_id = :id)"
                " AND NOT EXISTS (SELECT 1 FROM categories WHERE parent_id = :id)"
                " AND NOT EXISTS (SELECT 1 FROM category_attributes WHERE category_id = :id)"
            ).bindparams(id=category_id)
        )
