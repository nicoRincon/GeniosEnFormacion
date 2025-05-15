"""Create temas table

Revision ID: 55dca730399d
Revises: afa1906bff1a
Create Date: 2025-05-12 16:00:39.467703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55dca730399d'
down_revision = 'afa1906bff1a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('temas',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('id_materia', sa.Integer, sa.ForeignKey('materias.id'), nullable=False),
        sa.Column('nombre', sa.String(length=50), nullable=False),
        sa.Column('descripcion', sa.String(length=255)),
        sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
        sa.Column('fecha_actualizacion', sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_table('temas')
