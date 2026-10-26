"""empty message

Revision ID: fe081b7916a8
Revises: ff41682c72cd
Create Date: 2026-10-19 12:15:43.262777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe081b7916a8'
down_revision: Union[str, Sequence[str], None] = 'ff41682c72cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
