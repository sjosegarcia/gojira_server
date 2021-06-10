"""Chat model

Revision ID: 72f0cad66d03
Revises: d26502703bfa
Create Date: 2021-05-12 15:19:20.922580

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "72f0cad66d03"
down_revision = "d26502703bfa"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "chatmodel",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("chat_id", sa.NUMERIC(), nullable=True),
        sa.Column("created_on", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_on", sa.DateTime(timezone=True), nullable=False),
        sa.Column("welcome_message", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", "uuid"),
        sa.UniqueConstraint("uuid"),
        sa.UniqueConstraint("uuid"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("chatmodel")
    # ### end Alembic commands ###
