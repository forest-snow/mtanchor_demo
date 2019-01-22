"""empty message

Revision ID: 832ad7a3b174
Revises: 
Create Date: 2019-01-22 18:05:16.061050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '832ad7a3b174'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('start',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('anchors1', sa.String(), nullable=True),
    sa.Column('topics1', sa.String(), nullable=True),
    sa.Column('Q1', sa.String(), nullable=True),
    sa.Column('vocab1', sa.String(), nullable=True),
    sa.Column('index1', sa.String(), nullable=True),
    sa.Column('dict1', sa.String(), nullable=True),
    sa.Column('M_dev1', sa.String(), nullable=True),
    sa.Column('Y_dev1', sa.String(), nullable=True),
    sa.Column('anchors2', sa.String(), nullable=True),
    sa.Column('topics2', sa.String(), nullable=True),
    sa.Column('Q2', sa.String(), nullable=True),
    sa.Column('vocab2', sa.String(), nullable=True),
    sa.Column('index2', sa.String(), nullable=True),
    sa.Column('dict2', sa.String(), nullable=True),
    sa.Column('M_dev2', sa.String(), nullable=True),
    sa.Column('Y_dev2', sa.String(), nullable=True),
    sa.Column('intra1', sa.String(), nullable=True),
    sa.Column('cross1', sa.String(), nullable=True),
    sa.Column('intra2', sa.String(), nullable=True),
    sa.Column('cross2', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('update',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('anchors1', sa.String(), nullable=True),
    sa.Column('anchors2', sa.String(), nullable=True),
    sa.Column('topics1', sa.String(), nullable=True),
    sa.Column('topics2', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('intra1', sa.String(), nullable=True),
    sa.Column('cross1', sa.String(), nullable=True),
    sa.Column('intra2', sa.String(), nullable=True),
    sa.Column('cross2', sa.String(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('update')
    op.drop_table('user')
    op.drop_table('start')
    # ### end Alembic commands ###