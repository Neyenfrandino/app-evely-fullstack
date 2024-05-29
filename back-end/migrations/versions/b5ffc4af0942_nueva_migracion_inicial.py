"""Nueva migración inicial

Revision ID: b5ffc4af0942
Revises: 
Create Date: 2024-05-20 14:51:32.071522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5ffc4af0942'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pastillas_tabla', sa.Column('number_of_tablet_pills', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pastillas_tabla', 'number_of_tablet_pills')
    # ### end Alembic commands ###