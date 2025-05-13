"""Create materias table

Revision ID: 1a66334c7c96
Revises: 1c3d1e755e85
Create Date: 2025-05-12 15:59:17.083656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a66334c7c96'
down_revision = '1c3d1e755e85'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('materias',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.Column('descripcion', sa.String(length=255)),
        sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
        sa.Column('fecha_actualizacion', sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_table('materias')
