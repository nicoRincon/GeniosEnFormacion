"""Populate Roles

Revision ID: c84a78bf30cd
Revises: 6eeff10eac33
Create Date: 2025-05-21 17:24:03.628108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c84a78bf30cd'
down_revision = '6eeff10eac33'
branch_labels = None
depends_on = None


def upgrade():
    roles_table = sa.table(
        'roles',
        sa.column('nombre_rol', sa.String(50)),
    )
    op.bulk_insert(
        roles_table,
        [
            {'nombre_rol': 'Superadmin'},
            {'nombre_rol': 'Profesor'},
            {'nombre_rol': 'Estudiante'},
        ]
    )


def downgrade():
    op.execute(
        "DELETE FROM roles WHERE nombre_rol IN ('Superadmin', 'Profesor', 'Estudiante')"
    )
    # Opcional: resetear autoincremento (MySQL)
    op.execute("ALTER TABLE roles AUTO_INCREMENT = 1")
