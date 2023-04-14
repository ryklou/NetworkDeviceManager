"""Add type column to Device model

Revision ID: 28239997faa4
Revises: b4d96a98717e
Create Date: 2023-04-13 20:25:00.176619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28239997faa4'
down_revision = 'b4d96a98717e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('device', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=80), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('device', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###