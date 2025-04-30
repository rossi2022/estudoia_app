"""Corrigir modelos

Revision ID: bcaf9d1d9f68
Revises: ba04b3ccd5c9
Create Date: 2025-04-23 13:58:28.257225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcaf9d1d9f68'
down_revision: Union[str, None] = 'ba04b3ccd5c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
