"""add role colume to user table

Revision ID: 83907a17d815
Revises: 3bd6608e6bf8
Create Date: 2025-01-17 11:21:17.785147

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "83907a17d815"
down_revision: Union[str, None] = "3bd6608e6bf8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("role", sa.String(), server_default="user", nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "role")
    # ### end Alembic commands ###
