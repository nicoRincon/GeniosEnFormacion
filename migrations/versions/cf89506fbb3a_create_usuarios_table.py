"""Create usuarios table

Revision ID: cf89506fbb3a
Revises: 55dca730399d
Create Date: 2025-05-12 16:06:21.515907

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'cf89506fbb3a'
down_revision = '55dca730399d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('usuarios',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('id_rol', sa.String(20), sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('nombre', sa.String(50), nullable=False),
        sa.Column('apellido', sa.String(50), nullable=False),
        sa.Column('nombre_usuario', sa.String(100), unique=True, nullable=False),
        sa.Column('clave', sa.String(256), nullable=False),
        sa.Column('correo', sa.String(100), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), default=datetime.utcnow),
        sa.Column('fecha_actualizacion', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )



def downgrade():
    op.drop_table('usuarios')
