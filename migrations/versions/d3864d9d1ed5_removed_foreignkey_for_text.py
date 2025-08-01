"""removed ForeignKey for text

Revision ID: d3864d9d1ed5
Revises: 3b0f6684e9e6
Create Date: 2025-07-26 21:08:58.537576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3864d9d1ed5'
down_revision = '3b0f6684e9e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.alter_column('text',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.drop_constraint(batch_op.f('author_id_link'), type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('author_id_link'), 'user', ['text'], ['id'])
        batch_op.alter_column('text',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
