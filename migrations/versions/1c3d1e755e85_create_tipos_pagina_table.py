"""Create tipos_pagina table

Revision ID: 1c3d1e755e85
Revises: 26bd72ac0e3b
Create Date: 2025-05-12 15:57:28.269547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c3d1e755e85'
down_revision = '26bd72ac0e3b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tipos_pagina',
            sa.Column('id', sa.String(length=20), primary_key=True),
            sa.Column('nombre_tipo_pagina', sa.String(length=20), nullable=False)
    )          


def downgrade():
    op.drop_table('tipos_pagina')
