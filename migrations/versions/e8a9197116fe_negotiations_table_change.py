"""Negotiations Table Change

Revision ID: e8a9197116fe
Revises: ae5f84dd9fd8
Create Date: 2024-06-20 13:32:22.523711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8a9197116fe'
down_revision = 'ae5f84dd9fd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('negotiations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ad_id', sa.Integer(), nullable=False),
    sa.Column('new_amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['ad_id'], ['ad_request.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('negotiation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('negotiation',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('campaign_id', sa.INTEGER(), nullable=False),
    sa.Column('new_amount', sa.FLOAT(), nullable=False),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('negotiations')
    # ### end Alembic commands ###
