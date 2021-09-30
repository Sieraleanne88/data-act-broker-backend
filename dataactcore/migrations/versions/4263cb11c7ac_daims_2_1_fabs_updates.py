""" DAIMS 2.1 FABS Updates

Revision ID: 4263cb11c7ac
Revises: 6a7fa3623e2c
Create Date: 2021-07-27 20:58:11.286044

"""

# revision identifiers, used by Alembic.
revision = '4263cb11c7ac'
down_revision = '6a7fa3623e2c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('detached_award_financial_assistance', sa.Column('funding_opportunity_goals', sa.Text(), nullable=True))
    op.add_column('detached_award_financial_assistance', sa.Column('funding_opportunity_number', sa.Text(), nullable=True))
    op.add_column('detached_award_financial_assistance', sa.Column('indirect_federal_sharing', sa.Numeric(), nullable=True))
    op.add_column('published_award_financial_assistance', sa.Column('funding_opportunity_goals', sa.Text(), nullable=True))
    op.add_column('published_award_financial_assistance', sa.Column('funding_opportunity_number', sa.Text(), nullable=True))
    op.add_column('published_award_financial_assistance', sa.Column('indirect_federal_sharing', sa.Numeric(), nullable=True))
    op.create_index(op.f('ix_detached_award_financial_assistance_federal_action_obligation'),
                    'detached_award_financial_assistance', ['federal_action_obligation'], unique=False)
    op.create_index(op.f('ix_detached_award_financial_assistance_funding_opportunity_goals'),
                    'detached_award_financial_assistance', ['funding_opportunity_goals'], unique=False)
    op.create_index(op.f('ix_detached_award_financial_assistance_funding_opportunity_number'),
                    'detached_award_financial_assistance', ['funding_opportunity_number'], unique=False)
    op.create_index(op.f('ix_detached_award_financial_assistance_indirect_federal_sharing'),
                    'detached_award_financial_assistance', ['indirect_federal_sharing'], unique=False)
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_detached_award_financial_assistance_indirect_federal_sharing'),
                  table_name='detached_award_financial_assistance')
    op.drop_index(op.f('ix_detached_award_financial_assistance_funding_opportunity_number'),
                  table_name='detached_award_financial_assistance')
    op.drop_index(op.f('ix_detached_award_financial_assistance_funding_opportunity_goals'),
                  table_name='detached_award_financial_assistance')
    op.drop_index(op.f('ix_detached_award_financial_assistance_federal_action_obligation'),
                  table_name='detached_award_financial_assistance')
    op.drop_column('published_award_financial_assistance', 'indirect_federal_sharing')
    op.drop_column('published_award_financial_assistance', 'funding_opportunity_number')
    op.drop_column('published_award_financial_assistance', 'funding_opportunity_goals')
    op.drop_column('detached_award_financial_assistance', 'indirect_federal_sharing')
    op.drop_column('detached_award_financial_assistance', 'funding_opportunity_number')
    op.drop_column('detached_award_financial_assistance', 'funding_opportunity_goals')
    # ### end Alembic commands ###

