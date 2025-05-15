"""Create evaluaciones table

Revision ID: 25539aae9a37
Revises: 5ab2f247b9de
Create Date: 2025-05-12 16:17:01.834818

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '25539aae9a37'
down_revision = '5ab2f247b9de'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('evaluaciones',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_usuario', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('id_contenido', sa.Integer(), sa.ForeignKey('contenido.id'), nullable=False),
        sa.Column('titulo', sa.String(50), nullable=False),
        sa.Column('tipo_evaluacion', sa.String(10), nullable=False),
        sa.Column('lista_preguntas', sa.Text()),
        sa.Column('fecha_creacion', sa.DateTime(), default=datetime.utcnow),
        sa.Column('fecha_actualizacion', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )


def downgrade():
    op.drop_table('evaluaciones')
