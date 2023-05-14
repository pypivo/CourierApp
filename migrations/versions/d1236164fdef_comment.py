"""comment

Revision ID: d1236164fdef
Revises: 
Create Date: 2023-05-03 19:16:06.279488

"""
import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1236164fdef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('couriers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('courier_type', sa.Enum('FOOT', 'BIKE', 'AUTO', name='couriertypeenum'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('regions', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('completed_orders',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.Column('complete_time', sa.TIMESTAMP(timezone=datetime.timezone.utc), nullable=False),
    sa.ForeignKeyConstraint(['courier_id'], ['couriers.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('delivery_hours',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('delivery_hours', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('districts',
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['courier_id'], ['couriers.id'], ),
    sa.PrimaryKeyConstraint('courier_id', 'district_id')
    )
    op.create_table('work_times',
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.Column('work_time', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['courier_id'], ['couriers.id'], ),
    sa.PrimaryKeyConstraint('courier_id', 'work_time')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('work_times')
    op.drop_table('districts')
    op.drop_table('delivery_hours')
    op.drop_table('completed_orders')
    op.drop_table('orders')
    op.drop_table('couriers')
    # ### end Alembic commands ###