"""Agregar campos de regional y campaign

Revision ID: b96ccf2b7d15
Revises: 4175518ac57a
Create Date: 2024-11-13 19:20:18.148389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b96ccf2b7d15'
down_revision = '4175518ac57a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Data_Turnos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('regional', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('campaign', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Data_Turnos', schema=None) as batch_op:
        batch_op.drop_column('campaign')
        batch_op.drop_column('regional')

    # ### end Alembic commands ###
