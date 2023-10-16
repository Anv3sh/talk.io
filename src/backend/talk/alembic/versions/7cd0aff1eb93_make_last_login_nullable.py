"""make last login nullable

Revision ID: 7cd0aff1eb93
Revises: 
Create Date: 2023-10-16 07:33:31.047216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cd0aff1eb93'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "user"


def table_exists(table_name):
    # Check if the table exists
    conn = op.get_bind()
    return conn.dialect.has_table(conn, table_name)


def upgrade() -> None:
    if table_exists(table_name):
        op.alter_column(table_name,sa.Column("last_login_at"),existing_nullable=False,nullable=True)


def downgrade() -> None:
    if table_exists(table_name):
        op.alter_column(table_name,sa.Column("last_login_at"),existing_nullable=True,nullable=False)
