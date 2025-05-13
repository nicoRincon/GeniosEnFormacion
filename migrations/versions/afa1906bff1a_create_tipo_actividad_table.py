"""Create tipo_actividad table

Revision ID: afa1906bff1a
Revises: 1a66334c7c96
Create Date: 2025-05-12 16:00:02.970133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afa1906bff1a'
down_revision = '1a66334c7c96'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tipo_actividad',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('tipo_actividad', sa.String(length=50), nullable=False),
        sa.Column('peso', sa.Numeric(), nullable=True)
    )


def downgrade():
    op.drop_table('tipo_actividad')
