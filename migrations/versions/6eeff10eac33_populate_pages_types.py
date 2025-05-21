"""Populate Pages types

Revision ID: 6eeff10eac33
Revises: 3f19c1ea5c7d
Create Date: 2025-05-21 17:31:49.902360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eeff10eac33'
down_revision = '3f19c1ea5c7d'
branch_labels = None
depends_on = None


def upgrade():
    tipos_pagina_table = sa.table(
        'tipos_pagina',
        sa.column('nombre_tipo_pagina', sa.String(50)),
    )
    op.bulk_insert(
        tipos_pagina_table,
        [
            {'nombre_tipo_pagina': 'Modulo'},
            {'nombre_tipo_pagina': 'Paginas'},
            {'nombre_tipo_pagina': 'Sub-paginas'},
        ]
    )


def downgrade():
    op.execute(
        "DELETE FROM tipos_pagina WHERE nombre_tipo_pagina IN ('Modulo', 'Paginas', 'Sub-paginas')"
    )
    op.execute("ALTER TABLE tipos_pagina AUTO_INCREMENT = 1")