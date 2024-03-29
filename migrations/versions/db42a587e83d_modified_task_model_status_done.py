"""Modified task model, status_done is now required

Revision ID: db42a587e83d
Revises: 36214876a541
Create Date: 2023-12-26 14:27:14.894019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db42a587e83d'
down_revision = '36214876a541'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('status_done',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('status_done',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###
