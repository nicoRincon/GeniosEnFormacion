"""Create roles_x_pagina table

Revision ID: d0c96eab1f0f
Revises: 143630fb31c5
Create Date: 2025-05-12 16:21:47.484675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0c96eab1f0f'
down_revision = '143630fb31c5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('roles_x_pagina',
        sa.Column('id_rol', sa.Integer(), sa.ForeignKey('roles.id'), primary_key=True),
        sa.Column('id_pagina', sa.Integer(), sa.ForeignKey('paginas.id'), primary_key=True)
    )


def downgrade():
    op.drop_table('roles_x_pagina')
