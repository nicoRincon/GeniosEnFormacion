"""Create paginas table

Revision ID: 143630fb31c5
Revises: bee91f1a854b
Create Date: 2025-05-12 16:19:13.176339

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '143630fb31c5'
down_revision = 'bee91f1a854b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('paginas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('id_tipo_pagina', sa.String(20), sa.ForeignKey('tipos_pagina.id'), nullable=False),
        sa.Column('id_pagina_padre', sa.Integer(), sa.ForeignKey('paginas.id'), nullable=True),
        sa.Column('nombre_pagina', sa.String(80), nullable=False),
        sa.Column('descripcion', sa.String(80)),
        sa.Column('ruta', sa.String(20)),
        sa.Column('fecha_creacion', sa.DateTime(), default=datetime.utcnow),
        sa.Column('fecha_actualizacion', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )


def downgrade():
    op.drop_table('paginas')
