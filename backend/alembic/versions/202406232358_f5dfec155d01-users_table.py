"""users table

Revision ID: f5dfec155d01
Revises: 
Create Date: 2024-06-23 23:58:19.529466+02:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f5dfec155d01'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('gender', sa.Enum('male', 'female', 'other', name='usergender'), nullable=True),
        sa.Column('birth_year', sa.Integer(), nullable=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('banned_from_webapp', sa.Boolean(), server_default='False', nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        schema='data_entry'
    )
    op.create_index(op.f('ix_data_entry_users_id'), 'users', ['id'], unique=False, schema='data_entry')


def downgrade() -> None:
    op.drop_index(op.f('ix_data_entry_users_id'), table_name='users', schema='data_entry')
    op.drop_table('users', schema='data_entry')
    op.execute('DROP TYPE usergender')
