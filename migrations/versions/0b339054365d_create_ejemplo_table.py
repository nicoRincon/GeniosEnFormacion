"""Create ejemplo table

Revision ID: 0b339054365d
Revises: ed12f39e6658
Create Date: 2025-05-12 16:09:56.124520

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '0b339054365d'
down_revision = 'ed12f39e6658'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('ejemplos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('id_contenido', sa.Integer(), sa.ForeignKey('contenido.id'), nullable=False),
        sa.Column('ejemplos', sa.Text(), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), default=datetime.utcnow),
        sa.Column('fecha_actualizacion', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )


def downgrade():
    op.drop_table('ejemplos')
