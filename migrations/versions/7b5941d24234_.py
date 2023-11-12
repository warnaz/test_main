"""empty message

Revision ID: 7b5941d24234
Revises: 
Create Date: 2023-11-12 13:21:34.365103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b5941d24234'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('action_name', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('token', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('route',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('route_name', sa.String(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wallet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('primary_key', sa.String(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('action',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=False),
    sa.Column('action_list_id', sa.Integer(), nullable=False),
    sa.Column('pair', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['action_list_id'], ['action_list.id'], ),
    sa.ForeignKeyConstraint(['route_id'], ['route.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('action_wallet',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('gas', sa.Integer(), nullable=False),
    sa.Column('action_id', sa.Integer(), nullable=False),
    sa.Column('wallet_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('estimated_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('completed_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['action_id'], ['action.id'], ),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('desc', sa.String(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.Column('action_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['action_id'], ['action.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['route_id'], ['route.id'], ),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status')
    op.drop_table('action_wallet')
    op.drop_table('action')
    op.drop_table('wallet')
    op.drop_table('route')
    op.drop_table('project')
    op.drop_table('client')
    op.drop_table('action_list')
    # ### end Alembic commands ###