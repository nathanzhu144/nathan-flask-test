"""followers

Revision ID: 20507858a0bd
Revises: 24a126d1d80d
Create Date: 2020-08-04 11:47:40.259345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20507858a0bd'
down_revision = '24a126d1d80d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###