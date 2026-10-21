"""Rebuild search text now that Uzbek apostrophes are dropped and ё is read as е.

"Yoqilg'i filtri" used to be stored as "yoqilg i filtri", so "yoqilgi filtri" found nothing.

Revision ID: 20261021_0009
Revises: 20261021_0008
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.orm import Session

from alembic import op
from app.catalog import refresh_products
from app.models import Brand, Supplier
from app.normalization import normalize_text

revision: str = "20261021_0009"
down_revision: str | None = "20261021_0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    session = Session(bind=op.get_bind())
    refresh_products(session)
    for model in (Brand, Supplier):
        for row in session.query(model):
            row.normalized_name = normalize_text(row.name)
    session.flush()
    # Vehicle text is assembled from workbook columns that are no longer at hand; vehicle
    # names carry no apostrophes, so only ё needs folding.
    op.execute(sa.text("UPDATE vehicles SET normalized_text = replace(normalized_text, 'ё', 'е')"))


def downgrade() -> None:
    # Search text is derived data; the previous form is not worth reconstructing.
    pass
