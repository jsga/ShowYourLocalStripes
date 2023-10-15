"""Added currency

Revision ID: 4eebef954517
Revises: f9cea00240e0
Create Date: 2023-09-14 10:42:04.587573

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "4eebef954517"
down_revision = "f9cea00240e0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currency",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=True),
        sa.Column("gbp_to_eur", sa.Float(), nullable=True),
        sa.Column("gbp_to_usd", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("currency")
    # ### end Alembic commands ###