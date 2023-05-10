"""empty message

Revision ID: af7e8afec600
Revises: 
Create Date: 2023-05-02 21:46:51.227217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af7e8afec600'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_roles'))
    )
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_users'))
    )
    op.create_table('accounting',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('spent', sa.Integer(), nullable=False),
    sa.Column('paid', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name=op.f('fk_accounting_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_accounting'))
    )
    op.create_table('association_table',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_association_table_role_id_roles')),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name=op.f('fk_association_table_user_id_users'))
    )
    op.create_table('dialogues',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('top_p', sa.Float(), nullable=False),
    sa.Column('n', sa.Integer(), nullable=False),
    sa.Column('max_tokens', sa.Integer(), nullable=False),
    sa.Column('presence_penalty', sa.Float(), nullable=False),
    sa.Column('frequency_penalty', sa.Float(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name=op.f('fk_dialogues_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_dialogues'))
    )
    op.create_table('prompts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=False),
    sa.Column('owner', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['owner'], ['users.user_id'], name=op.f('fk_prompts_owner_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_prompts'))
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('dialogue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dialogue_id'], ['dialogues.id'], name=op.f('fk_messages_dialogue_id_dialogues')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('prompts')
    op.drop_table('dialogues')
    op.drop_table('association_table')
    op.drop_table('accounting')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###