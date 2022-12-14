"""shared notes

Revision ID: 4f73ad516b80
Revises: 1f3b98a6a297
Create Date: 2022-12-21 18:52:27.545430

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '4f73ad516b80'
down_revision = '1f3b98a6a297'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('share', 'note_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('share', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_index('ix_share_id', table_name='share')
    op.drop_column('share', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('share', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_index('ix_share_id', 'share', ['id'], unique=False)
    op.alter_column('share', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('share', 'note_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
