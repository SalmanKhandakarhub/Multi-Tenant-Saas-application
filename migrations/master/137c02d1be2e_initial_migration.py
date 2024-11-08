"""Initial migration

Revision ID: 137c02d1be2e
Revises: eb001d32ad2e
Create Date: 2024-10-29 10:53:41.535884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '137c02d1be2e'
down_revision: Union[str, None] = 'eb001d32ad2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('permissions', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('subscription_plans', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('subscription_products', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('tenant_subscriptions', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('tenants', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_delete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_delete')
    op.drop_column('tenants', 'is_delete')
    op.drop_column('tenant_subscriptions', 'is_delete')
    op.drop_column('subscription_products', 'is_delete')
    op.drop_column('subscription_plans', 'is_delete')
    op.drop_column('roles', 'is_delete')
    op.drop_column('permissions', 'is_delete')
    # ### end Alembic commands ###
