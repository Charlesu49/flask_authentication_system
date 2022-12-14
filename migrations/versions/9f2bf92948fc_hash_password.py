"""hash password

Revision ID: 9f2bf92948fc
Revises: e15b394701aa
Create Date: 2022-08-14 18:35:35.939337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f2bf92948fc'
down_revision = 'e15b394701aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hash_password', sa.String(length=255), nullable=False))
    op.drop_column('user', 'password_salt')
    op.drop_column('user', 'password_hash_algorithm')
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=255), nullable=False))
    op.add_column('user', sa.Column('password_hash_algorithm', sa.VARCHAR(length=255), nullable=True))
    op.add_column('user', sa.Column('password_salt', sa.VARCHAR(length=255), nullable=True))
    op.drop_column('user', 'hash_password')
    # ### end Alembic commands ###
