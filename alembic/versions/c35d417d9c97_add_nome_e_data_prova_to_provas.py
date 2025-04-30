"""add nome e data_prova to provas

Revision ID: c35d417d9c97
Revises: bcaf9d1d9f68
Create Date: 2025-04-28 10:35:59.911910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c35d417d9c97'
down_revision: Union[str, None] = 'bcaf9d1d9f68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
