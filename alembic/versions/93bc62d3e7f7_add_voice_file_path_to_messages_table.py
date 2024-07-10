"""add voice_file_path to messages table

Revision ID: 93bc62d3e7f7
Revises: 1d526b4ff1f5
Create Date: 2024-07-04 16:29:16.814494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93bc62d3e7f7'
down_revision: Union[str, None] = '1d526b4ff1f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('voice_file_path', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('messages', 'voice_file_path')
