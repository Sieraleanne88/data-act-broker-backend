"""Add upper UEI indexes to tables

Revision ID: 4d64c79360af
Revises: 9e295cff8733
Create Date: 2021-08-05 12:27:08.745832

"""

# revision identifiers, used by Alembic.
revision = '4d64c79360af'
down_revision = '9e295cff8733'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import text


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_pafa_uei_upper', 'published_award_financial_assistance', [text('UPPER(uei)')], unique=False)
    op.create_index('ix_dafa_uei_upper', 'detached_award_financial_assistance', [text('UPPER(uei)')], unique=False)
    op.create_index('ix_dap_awardee_or_recipient_uei_upper', 'detached_award_procurement', [text('UPPER(awardee_or_recipient_uei)')], unique=False)
    op.create_index('ix_duns_uei_upper', 'duns', [text('UPPER(uei)')], unique=False)
    op.create_index('ix_historic_duns_uei_upper', 'historic_duns', [text('UPPER(uei)')], unique=False)
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_historic_duns_uei_upper', table_name='historic_duns')
    op.drop_index('ix_duns_uei_upper', table_name='duns')
    op.drop_index('ix_dap_awardee_or_recipient_uei_upper', table_name='detached_award_procurement')
    op.drop_index('ix_dafa_uei_upper', table_name='detached_award_financial_assistance')
    op.drop_index('ix_pafa_uei_upper', table_name='published_award_financial_assistance')
    # ### end Alembic commands ###

