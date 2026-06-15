"""add latest_resume_text to users

Revision ID: 3903fcb62707
Revises: 36dc63be2611
Create Date: 2026-06-13 14:44:25.998410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3903fcb62707'
down_revision: Union[str, Sequence[str], None] = '36dc63be2611'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add username as nullable first
    op.add_column('users', sa.Column('username', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('latest_resume_text', sa.Text(), nullable=True))

    # fill existing rows with a default username based on email
    op.execute("UPDATE users SET username = split_part(email, '@', 1) || '_' || id WHERE username IS NULL")

    # now make username not null and unique
    op.alter_column('users', 'username', nullable=False)
    op.create_unique_constraint('uq_users_username', 'users', ['username'])

    # update email column length
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=100),
               existing_nullable=False)

    # drop old full_name column
    op.drop_column('users', 'full_name')


def downgrade() -> None:
    op.add_column('users', sa.Column('full_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_constraint('uq_users_username', 'users', type_='unique')
    op.alter_column('users', 'email',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
    op.drop_column('users', 'latest_resume_text')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'username')