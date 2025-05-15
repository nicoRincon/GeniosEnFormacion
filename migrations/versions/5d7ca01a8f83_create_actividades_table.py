"""Create actividades table

Revision ID: 5d7ca01a8f83
Revises: 0b339054365d
Create Date: 2025-05-12 16:12:56.959136

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '5d7ca01a8f83'
down_revision = '0b339054365d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('actividades',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_contenido', sa.Integer(), sa.ForeignKey('contenido.id'), nullable=False),
        sa.Column('id_tipo_actividad', sa.Integer(), sa.ForeignKey('tipo_actividad.id'), nullable=False),
        sa.Column('contenido', sa.Text(), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), default=datetime.utcnow),
        sa.Column('fecha_actualizacion', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )

def downgrade():
    op.drop_table('actividades')
