"""dataset_management

Revision ID: 002
Revises: 001
Create Date: 2026-07-26 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Datasets Table
    op.create_table('datasets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('original_filename', sa.String(length=500), nullable=False),
        sa.Column('stored_filename', sa.String(length=500), nullable=False),
        sa.Column('display_name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('file_type', sa.Enum('CSV', 'EXCEL', name='filetype'), nullable=False),
        sa.Column('file_size_bytes', sa.BigInteger(), nullable=False),
        sa.Column('storage_path', sa.String(length=1000), nullable=False),
        sa.Column('processing_status', sa.Enum('UPLOADING', 'PROCESSING', 'READY', 'FAILED', name='processingstatus'), nullable=False),
        sa.Column('visibility', sa.Enum('PRIVATE', 'ORGANIZATION', 'PUBLIC', name='visibility'), nullable=False),
        sa.Column('encoding', sa.String(length=20), nullable=True),
        sa.Column('delimiter', sa.String(length=5), nullable=True),
        sa.Column('row_count', sa.Integer(), nullable=True),
        sa.Column('column_count', sa.Integer(), nullable=True),
        sa.Column('checksum_sha256', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_datasets_id'), 'datasets', ['id'], unique=False)
    op.create_index(op.f('ix_datasets_owner_id'), 'datasets', ['owner_id'], unique=False)
    op.create_index(op.f('ix_datasets_stored_filename'), 'datasets', ['stored_filename'], unique=True)
    op.create_index(op.f('ix_datasets_checksum_sha256'), 'datasets', ['checksum_sha256'], unique=False)

    # Dataset Columns Table
    op.create_table('dataset_columns',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dataset_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('column_name', sa.String(length=255), nullable=False),
        sa.Column('detected_data_type', sa.Enum('INTEGER', 'FLOAT', 'BOOLEAN', 'STRING', 'DATE', 'DATETIME', 'CATEGORICAL', 'MIXED', 'UNKNOWN', name='columndatatype'), nullable=False),
        sa.Column('is_nullable', sa.Boolean(), nullable=False),
        sa.Column('is_unique', sa.Boolean(), nullable=False),
        sa.Column('sample_values', sa.String(length=1000), nullable=True),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dataset_columns_dataset_id'), 'dataset_columns', ['dataset_id'], unique=False)
    op.create_index(op.f('ix_dataset_columns_id'), 'dataset_columns', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_dataset_columns_id'), table_name='dataset_columns')
    op.drop_index(op.f('ix_dataset_columns_dataset_id'), table_name='dataset_columns')
    op.drop_table('dataset_columns')
    
    op.drop_index(op.f('ix_datasets_checksum_sha256'), table_name='datasets')
    op.drop_index(op.f('ix_datasets_stored_filename'), table_name='datasets')
    op.drop_index(op.f('ix_datasets_owner_id'), table_name='datasets')
    op.drop_index(op.f('ix_datasets_id'), table_name='datasets')
    op.drop_table('datasets')
    
    op.execute('DROP TYPE columndatatype')
    op.execute('DROP TYPE filetype')
    op.execute('DROP TYPE processingstatus')
    op.execute('DROP TYPE visibility')
