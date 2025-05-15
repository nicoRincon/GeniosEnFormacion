"""Create Roles table

Revision ID: 26bd72ac0e3b
Revises: 
Create Date: 2025-05-12 15:56:09.773356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26bd72ac0e3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('roles',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre_rol', sa.String(length=20), nullable=False)
    )


def downgrade():
    op.drop_table('roles') 
