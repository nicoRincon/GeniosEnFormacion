"""Create notas_x_contenido table

Revision ID: bee91f1a854b
Revises: 25539aae9a37
Create Date: 2025-05-12 16:18:29.985127

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'bee91f1a854b'
down_revision = '25539aae9a37'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('notas_x_contenido',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('id_usuario', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('id_contenido', sa.Integer(), sa.ForeignKey('contenido.id'), nullable=False),
        sa.Column('nota_obtenida', sa.Numeric()),
        sa.Column('fecha_creacion', sa.DateTime(), default=datetime.utcnow),
        sa.Column('fecha_actualizacion', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )



def downgrade():
    op.drop_table('notas_x_contenido')
