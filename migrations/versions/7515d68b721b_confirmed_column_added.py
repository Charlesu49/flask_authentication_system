"""confirmed column added

Revision ID: 7515d68b721b
Revises: 1cf1ef75be86
Create Date: 2022-08-24 02:36:22.879419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7515d68b721b'
down_revision = '1cf1ef75be86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('confirmed', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_column('user', 'confirmed')
    # ### end Alembic commands ###