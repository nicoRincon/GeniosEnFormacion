"""Populate activity types

Revision ID: f4a1497712cf
Revises: 64d3d4b6148d
Create Date: 2025-05-27 00:01:45.783561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4a1497712cf'
down_revision = '64d3d4b6148d'
branch_labels = None
depends_on = None


def upgrade():
    activity_types_table = sa.table(
        'tipo_actividad',
        sa.column('tipo_actividad', sa.String(50)),
        sa.column('peso', sa.Numeric),
    )
    op.bulk_insert(
        activity_types_table,
        [
            {'tipo_actividad': 'Evaluación', 'peso': 1.0},
            {'tipo_actividad': 'Actividad', 'peso': 0.5},
            {'tipo_actividad': 'Evaluación final', 'peso': 2.0},
        ]
    )


def downgrade():
    op.execute(
        "DELETE FROM tipo_actividad WHERE tipo_actividad IN ('Evaluación', 'Actividad', 'Evaluación final')"
    )
    op.execute("ALTER TABLE tipo_actividad AUTO_INCREMENT = 1")
