"""modify tenant relations

Revision ID: f4a7a186e01e
Revises: 167f3ea201c9
Create Date: 2024-10-29 10:56:22.077803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4a7a186e01e'
down_revision: Union[str, None] = '167f3ea201c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('branches', sa.Column('location', sa.String(length=64), nullable=True))
    op.add_column('branches', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('branches', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('branches', sa.Column('creared_by', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'branches', 'users', ['creared_by'], ['id'])
    op.add_column('files', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('logs', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('notifications', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('organizations', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('permissions', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('is_delete', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_super_admin', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_delete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_delete')
    op.drop_column('users', 'is_super_admin')
    op.drop_column('roles', 'is_delete')
    op.drop_column('permissions', 'is_delete')
    op.drop_column('organizations', 'is_delete')
    op.drop_column('notifications', 'is_delete')
    op.drop_column('logs', 'is_delete')
    op.drop_column('files', 'is_delete')
    op.drop_constraint(None, 'branches', type_='foreignkey')
    op.drop_column('branches', 'creared_by')
    op.drop_column('branches', 'is_delete')
    op.drop_column('branches', 'is_active')
    op.drop_column('branches', 'location')
    # ### end Alembic commands ###