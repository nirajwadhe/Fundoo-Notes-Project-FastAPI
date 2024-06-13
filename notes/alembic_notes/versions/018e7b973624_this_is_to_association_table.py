"""This is to Association table

Revision ID: 018e7b973624
Revises: 559088d55431
Create Date: 2024-06-13 11:42:35.772839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '018e7b973624'
down_revision: Union[str, None] = '559088d55431'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('label_association',
    sa.Column('notes_id', sa.BigInteger(), nullable=True),
    sa.Column('labels_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['labels_id'], ['labels.labels_id'], ),
    sa.ForeignKeyConstraint(['notes_id'], ['notes.notes_id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('label_association')
    # ### end Alembic commands ###
