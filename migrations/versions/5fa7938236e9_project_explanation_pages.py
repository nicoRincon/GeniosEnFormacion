"""Project explanation pages

Revision ID: 5fa7938236e9
Revises: 64d3d4b6148d
Create Date: 2025-05-21 15:44:07.632799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fa7938236e9'
down_revision = '64d3d4b6148d'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    result = conn.execute(
        sa.text("""
            INSERT INTO paginas (id_tipo_pagina, id_pagina_padre, nombre_pagina, descripcion, ruta)
            VALUES (:tipo, :padre, :nombre, :desc, :ruta)
            """
        ),
        {
            "tipo": 1,
            "padre": None,
            "nombre": "Entendimiento del Negocio",
            "desc": "Entendimiento del Negocio",
            "ruta": None
        }
    )
    inserted_id = result.lastrowid

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
                'id_tipo_pagina': 2,
                'id_pagina_padre': inserted_id,
                'nombre_pagina': 'Entendimiento del Negocio',
                'descripcion': 'Página de objetivos y preguntas clave del negocio',
                'ruta': 'business_understanding'
            },
            {
                'id_tipo_pagina': 2,
                'id_pagina_padre': inserted_id,
                'nombre_pagina': 'Ingeniería de Datos',
                'descripcion': 'Página sobre la ingeniería de datos del proyecto',
                'ruta': 'data_engineering'
            },
            {
                'id_tipo_pagina': 2,
                'id_pagina_padre': inserted_id,
                'nombre_pagina': 'Ingeniería de Modelos',
                'descripcion': 'Página sobre la ingeniería de modelos del proyecto',
                'ruta': 'model_engineering'
            },
            {
                'id_tipo_pagina': 2,
                'id_pagina_padre': inserted_id,
                'nombre_pagina': 'Evaluación de Modelos',
                'descripcion': 'Página sobre la evaluación de modelos del proyecto',
                'ruta': 'model_evaluation'
            },
            {
                'id_tipo_pagina': 2,
                'id_pagina_padre': inserted_id,
                'nombre_pagina': 'Despliegue de Modelos',
                'descripcion': 'Página sobre el despliegue de modelos del proyecto',
                'ruta': 'model_deployment'
            }
        ]
    )


def downgrade():
    conn = op.get_bind()

    result = conn.execute(
        sa.text("SELECT id FROM paginas WHERE nombre_pagina = 'Entendimiento del Negocio'")
    )
    ids = [row[0] for row in result.fetchall()]

    if ids:
        conn.execute(
            sa.text("DELETE FROM paginas WHERE id_pagina_padre IN :ids"),
            {"ids": tuple(ids)}
        )
        # 3. Elimina la página principal
        conn.execute(
            sa.text("DELETE FROM paginas WHERE id IN :ids"),
            {"ids": tuple(ids)}
        )
        last_id = ids[-1]
        conn.execute(sa.text(f'ALTER TABLE paginas AUTO_INCREMENT = {last_id}'))

