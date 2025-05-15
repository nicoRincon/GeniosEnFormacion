"""Create usuarios_x_materia table

Revision ID: dadc0367b2c3
Revises: cf89506fbb3a
Create Date: 2025-05-12 16:08:18.878347

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'dadc0367b2c3'
down_revision = 'cf89506fbb3a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('usuarios_x_materia',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_usuario', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('id_materia', sa.Integer(), sa.ForeignKey('materias.id'), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), default=datetime.utcnow),
        sa.Column('fecha_actualizacion', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )

def downgrade():
    op.drop_table('usuarios_x_materia')
