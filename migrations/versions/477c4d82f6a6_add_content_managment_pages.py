"""Add content managment pages

Revision ID: 477c4d82f6a6
Revises: f4a1497712cf
Create Date: 2025-05-27 01:45:48.606769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '477c4d82f6a6'
down_revision = 'f4a1497712cf'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # 1. Insertar la página principal
    result =conn.execute(
        sa.text("""
            INSERT INTO paginas (id_tipo_pagina, id_pagina_padre, nombre_pagina, descripcion, ruta)
            VALUES (:tipo, :padre, :nombre, :desc, :ruta)
        """),
        {
            "tipo": 1,
            "padre": None,
            "nombre": "Gestión de Contenido",
            "desc": "Gestión de Contenido",
            "ruta": None
        }
    )
    module_id = result.lastrowid

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
                "nombre_pagina": "Materias",
                "descripcion": "Gestión de Materias",
                "ruta": "subjects"
            },
            {
                "id_tipo_pagina": 2,
                "id_pagina_padre": module_id,
                "nombre_pagina": "Temas",
                "descripcion": "Gestión de Temas",
                "ruta": "topics"
            },
            {
                "id_tipo_pagina": 2,
                "id_pagina_padre": module_id,
                "nombre_pagina": "Contenidos",
                "descripcion": "Gestión de Contenidos",
                "ruta": "contents"
            },
            {
                "id_tipo_pagina": 2,
                "id_pagina_padre": module_id,
                "nombre_pagina": "Actividades",
                "descripcion": "Gestión de Actividades",
                "ruta": "activities"
            },
        ]
    )


def downgrade():
    conn = op.get_bind()

    result = conn.execute(
        sa.text("SELECT id FROM paginas WHERE nombre_pagina = 'Gestión de Contenido'")
    )
    ids = [row[0] for row in result.fetchall()]

    if ids:
        conn.execute(
            sa.text("DELETE FROM paginas WHERE id_pagina_padre IN :ids"),
            {"ids": tuple(ids)}
        )
        conn.execute(
            sa.text("DELETE FROM paginas WHERE id IN :ids"),
            {"ids": tuple(ids)}
        )
        last_id = ids[-1]
        conn.execute(sa.text(f'ALTER TABLE paginas AUTO_INCREMENT = {last_id}'))

