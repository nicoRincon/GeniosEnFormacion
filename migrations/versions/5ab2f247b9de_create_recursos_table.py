"""Create recursos table

Revision ID: 5ab2f247b9de
Revises: 5d7ca01a8f83
Create Date: 2025-05-12 16:13:40.018468

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '5ab2f247b9de'
down_revision = '5d7ca01a8f83'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('recursos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_actividad', sa.Integer(), sa.ForeignKey('actividades.id'), nullable=False),
        sa.Column('titulo', sa.String(50), nullable=False),
        sa.Column('tipo', sa.String(10), nullable=False),
        sa.Column('contenido', sa.String(255), nullable=False),
        sa.Column('descripcion', sa.String(255)),
        sa.Column('fecha_creacion', sa.DateTime(), default=datetime.utcnow),
        sa.Column('fecha_actualizacion', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )


def downgrade():
    op.drop_table('recursos')