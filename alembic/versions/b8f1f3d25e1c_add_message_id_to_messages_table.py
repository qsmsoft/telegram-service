"""add message_id to messages table

Revision ID: b8f1f3d25e1c
Revises: 74d414235cae
Create Date: 2024-09-13 15:48:44.460915

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b8f1f3d25e1c'
down_revision: Union[str, None] = '74d414235cae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('message_id', sa.BigInteger(), nullable=True))


def downgrade() -> None:
    op.drop_column('messages', 'message_id')
