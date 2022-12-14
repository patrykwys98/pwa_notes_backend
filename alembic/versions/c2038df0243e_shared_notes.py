"""shared notes

Revision ID: c2038df0243e
Revises: 9834acc573ea
Create Date: 2022-12-20 22:36:26.812009

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'c2038df0243e'
down_revision = '9834acc573ea'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('share_note_fkey', 'share', type_='foreignkey')
    op.drop_constraint('share_user_fkey', 'share', type_='foreignkey')
    op.drop_column('share', 'note')
    op.drop_column('share', 'user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('share', sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('share', sa.Column('note', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('share_user_fkey', 'share', 'user', ['user'], ['id'])
    op.create_foreign_key('share_note_fkey', 'share', 'note', ['note'], ['id'])
    # ### end Alembic commands ###
