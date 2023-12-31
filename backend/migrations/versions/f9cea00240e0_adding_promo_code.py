"""Adding promo code

Revision ID: f9cea00240e0
Revises: b6f5f7fa629a
Create Date: 2023-09-01 11:18:47.221177

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "f9cea00240e0"
down_revision = "b6f5f7fa629a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "store",
        sa.Column("promo_code", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("store", "promo_code")
    # ### end Alembic commands ###
