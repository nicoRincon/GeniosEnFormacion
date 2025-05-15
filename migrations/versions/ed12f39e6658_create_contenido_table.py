"""Create contenido table

Revision ID: ed12f39e6658
Revises: dadc0367b2c3
Create Date: 2025-05-12 16:09:07.291438

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'ed12f39e6658'
down_revision = 'dadc0367b2c3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('contenido',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_tema', sa.Integer(), sa.ForeignKey('temas.id'), nullable=False),
        sa.Column('titulo', sa.String(100), nullable=False),
        sa.Column('contenido', sa.Text(), nullable=False),
        sa.Column('nivel_grado', sa.Numeric()),
        sa.Column('fecha_creacion', sa.DateTime(), default=datetime.utcnow),
        sa.Column('fecha_actualizacion', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )


def downgrade():
    op.drop_table('contenido')
