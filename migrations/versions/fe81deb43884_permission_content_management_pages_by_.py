"""Permission content management pages by superadmin role

Revision ID: fe81deb43884
Revises: 477c4d82f6a6
Create Date: 2025-05-27 01:58:54.103770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe81deb43884'
down_revision = '477c4d82f6a6'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    result = conn.execute(
        sa.text("""
                select
                    m.id
                from
                    paginas m
                where
                    m.nombre_pagina = 'Gestión de Contenido'
                union
                select
                    p.id
                from
                    paginas m
                inner join paginas p on
                    p.id_pagina_padre = m.id
                where
                    m.nombre_pagina = 'Gestión de Contenido'"""
        )
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
        sa.text("""
            select
                m.id
            from
                paginas m
            where
                m.nombre_pagina = 'Gestión de Contenido'
            union
            select
                p.id
            from
                paginas m
            inner join paginas p on
                p.id_pagina_padre = m.id
            where
                m.nombre_pagina = 'Gestión de Contenido'"""
        )
    )

    ids = [row[0] for row in result.fetchall()]

    conn.execute(
        sa.text("DELETE FROM roles_x_pagina WHERE id_rol = 1 AND id_pagina IN :ids"),
        {"ids": tuple(ids)}
    )