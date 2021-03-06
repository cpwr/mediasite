"""empty message

Revision ID: 326b787cdb4
Revises: 1d3a934d9a4
Create Date: 2015-12-30 23:33:53.778713

"""

# revision identifiers, used by Alembic.
revision = '326b787cdb4'
down_revision = '1d3a934d9a4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=64), nullable=True))
    op.drop_index('ix_users_is_admin', table_name='users')
    op.drop_index('ix_users_login', table_name='users')
    op.drop_index('ix_users_name', table_name='users')
    op.drop_index('ix_users_reg_date', table_name='users')
    op.create_unique_constraint(None, 'users', ['username'])
    op.drop_column('users', 'name')
    op.drop_column('users', 'login')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('login', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_index('ix_users_reg_date', 'users', ['reg_date'], unique=False)
    op.create_index('ix_users_name', 'users', ['name'], unique=False)
    op.create_index('ix_users_login', 'users', ['login'], unique=True)
    op.create_index('ix_users_is_admin', 'users', ['is_admin'], unique=False)
    op.drop_column('users', 'username')
    ### end Alembic commands ###
