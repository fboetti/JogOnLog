"""sports tables

Revision ID: 246d89e95737
Revises: f5dfec155d01
Create Date: 2024-06-26 00:47:18.607124+02:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '246d89e95737'
down_revision: Union[str, None] = 'f5dfec155d01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Installing schema partition_manager and pg_partman extension
    op.execute("create schema if not exists partition_manager;")
    op.execute("create extension if not exists pg_partman schema partition_manager version '5.0.0';")

    op.create_table(
        'sports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('kcal_per_hour', sa.Float(), nullable=True),
        sa.Column('custom_properties', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='data_entry'
    )
    op.create_index(op.f('ix_data_entry_sports_id'), 'sports', ['id'], unique=True, schema='data_entry')
    op.create_index(op.f('ix_data_entry_sports_name'), 'sports', ['name'], unique=True, schema='data_entry')

    op.execute(
        """
            create sequence if not exists data_entry.sport_activities_id_seq;
        """
    )
    op.create_table(
        'sport_activities',
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            server_default=sa.text('nextval(\'data_entry.sport_activities_id_seq\'::regclass)'),
        ),
        sa.Column('id_sport', sa.Integer(), nullable=False),
        sa.Column('id_user', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('cost', sa.Float(), nullable=True),
        sa.Column('custom_properties', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['id_sport'], ['data_entry.sports.id'], ondelete='cascade'),
        sa.ForeignKeyConstraint(['id_user'], ['data_entry.users.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id_sport', 'id_user', 'start_time', name='sport_activities_pkey'),
        schema='data_entry',
        postgresql_partition_by='RANGE (start_time)'
    )
    op.create_index(op.f('ix_data_entry_sport_activities_id'), 'sport_activities', ['id'], unique=False, schema='data_entry')

    op.execute(
        """
            select partition_manager.create_parent(
                'data_entry.sport_activities',
                'start_time',
                '1 year'
            );
        """
    )


def downgrade() -> None:
    op.drop_table('sport_activities', schema='data_entry')
    op.drop_index(op.f('ix_data_entry_sports_name'), table_name='sports', schema='data_entry')
    op.drop_index(op.f('ix_data_entry_sports_id'), table_name='sports', schema='data_entry')
    op.drop_table('sports', schema='data_entry')

    op.execute('drop extension if exists pg_partman cascade;')
    op.execute('drop schema if exists partition_manager cascade;')
