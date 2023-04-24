"""empty message

Revision ID: b555da1c7745
Revises: 3564796c9f97
Create Date: 2023-04-13 21:17:55.434600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b555da1c7745'
down_revision = '3564796c9f97'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('role', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'role')
    # ### end Alembic commands ###