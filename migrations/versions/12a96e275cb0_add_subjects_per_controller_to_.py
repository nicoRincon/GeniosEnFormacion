"""Add subjects per controller to superadminrol

Revision ID: 12a96e275cb0
Revises: fe81deb43884
Create Date: 2025-05-27 13:28:29.123043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12a96e275cb0'
down_revision = 'fe81deb43884'
branch_labels = None
depends_on = None

name_page = 'Asignación de materias a usuarios'
def upgrade():
    conn = op.get_bind()

    # 1. Insertar la página principal
    result = conn.execute(
        sa.text("SELECT id FROM paginas WHERE nombre_pagina = 'Gestión de Contenido'")
    )
    module_id = result.fetchone()[0]

    op.bulk_insert(
        sa.table(
            'paginas',
            sa.column('id_tipo_pagina', sa.Integer),
            sa.column('id_pagina_padre', sa.Integer),
            sa.column('nombre_pagina', sa.String(80)),
            sa.column('descripcion', sa.String(80)),
            sa.column('ruta', sa.String(20)),
        ),
        [
            {
                "id_tipo_pagina": 2,
                "id_pagina_padre": module_id,
                "nombre_pagina": name_page,
                "descripcion": "Gestión de Materias",
                "ruta": "subjects_per_login"
            },
        ]
    )

    op.bulk_insert(
        sa.table(
            'roles_x_pagina',
            sa.column('id_rol', sa.Integer),
            sa.column('id_pagina', sa.Integer),
        ),
        [{
            "id_rol": 1,
            "id_pagina": conn.execute(
                sa.text(f"SELECT id FROM paginas WHERE nombre_pagina = '{name_page}'")
            ).fetchone()[0]
        }]
    )


def downgrade():
    conn = op.get_bind()
    result = conn.execute(
        sa.text(f"SELECT id FROM paginas WHERE nombre_pagina = '{name_page}'")
    )
    last_id = result.fetchone()[0]

    conn.execute(
        sa.text("DELETE FROM roles_x_pagina WHERE id_pagina = :page_id"),
        {"page_id": last_id}
    )

    conn.execute(
        sa.text("DELETE FROM paginas WHERE id = :page_id"),
        {"page_id": last_id}
    )
    conn.execute(sa.text(f'ALTER TABLE paginas AUTO_INCREMENT = {last_id}'))
