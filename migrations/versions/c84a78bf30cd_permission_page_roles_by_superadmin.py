"""Permission page roles by superadmin

Revision ID: c84a78bf30cd
Revises: 6eeff10eac33
Create Date: 2025-05-21 15:48:04.654182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c84a78bf30cd'
down_revision = '6eeff10eac33'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    result = conn.execute(
        sa.text("SELECT id FROM paginas WHERE nombre_pagina = 'Entendimiento del Negocio'")
    )
    rol_pages = [{ 'id_rol': 1, 'id_pagina': row[0] } for row in result.fetchall()]

    op.bulk_insert(
        sa.table(
            'roles_x_pagina',
            sa.column('id_rol', sa.Integer),
            sa.column('id_pagina', sa.Integer),
        ),
        rol_pages
    )


def downgrade():
    conn = op.get_bind()
    result = conn.execute(
        sa.text("SELECT id FROM paginas WHERE nombre_pagina = 'Entendimiento del Negocio'")
    )

    ids = [row[0] for row in result.fetchall()]

    conn.execute(
        sa.text("DELETE FROM roles_x_pagina WHERE id_rol = 1 AND id_pagina IN :ids"),
        {"ids": tuple(ids)}
    )
