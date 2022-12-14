"""added default and permissions column to Role

Revision ID: c6e4b39f0b06
Revises: 7515d68b721b
Create Date: 2022-08-30 15:25:15.335397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6e4b39f0b06'
down_revision = '7515d68b721b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('role', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('role', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_role_default'), 'role', ['default'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_role_default'), table_name='role')
    op.drop_column('role', 'permissions')
    op.drop_column('role', 'default')
    # ### end Alembic commands ###
