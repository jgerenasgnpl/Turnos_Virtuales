"""Agregar campo fecha_creacion a Turno

Revision ID: 4175518ac57a
Revises: 
Create Date: 2024-11-12 21:53:55.482351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4175518ac57a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Data_Turnos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha_gestion', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('fecha_creacion', sa.DateTime(), nullable=True))
        batch_op.alter_column('nombre',
               existing_type=sa.NCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               type_=sa.String(length=50),
               nullable=False)
        batch_op.alter_column('telefono',
               existing_type=sa.NCHAR(length=20, collation='Modern_Spanish_CI_AS'),
               type_=sa.String(length=20),
               nullable=False)
        batch_op.alter_column('correo',
               existing_type=sa.NCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               type_=sa.String(length=50),
               nullable=False)
        batch_op.alter_column('tipo_gestion',
               existing_type=sa.NCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('pago_cuotas',
               existing_type=sa.NCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('observacion',
               existing_type=sa.NCHAR(length=255, collation='Modern_Spanish_CI_AS'),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Data_Turnos', schema=None) as batch_op:
        batch_op.alter_column('observacion',
               existing_type=sa.String(length=255),
               type_=sa.NCHAR(length=255, collation='Modern_Spanish_CI_AS'),
               existing_nullable=True)
        batch_op.alter_column('pago_cuotas',
               existing_type=sa.String(length=50),
               type_=sa.NCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               existing_nullable=True)
        batch_op.alter_column('tipo_gestion',
               existing_type=sa.String(length=50),
               type_=sa.NCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               existing_nullable=True)
        batch_op.alter_column('correo',
               existing_type=sa.String(length=50),
               type_=sa.NCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               nullable=True)
        batch_op.alter_column('telefono',
               existing_type=sa.String(length=20),
               type_=sa.NCHAR(length=20, collation='Modern_Spanish_CI_AS'),
               nullable=True)
        batch_op.alter_column('nombre',
               existing_type=sa.String(length=50),
               type_=sa.NCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               nullable=True)
        batch_op.drop_column('fecha_creacion')
        batch_op.drop_column('fecha_gestion')

    # ### end Alembic commands ###