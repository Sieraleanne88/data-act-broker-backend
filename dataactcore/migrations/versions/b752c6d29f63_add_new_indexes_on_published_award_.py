"""Add new indexes on published_award_financial_assistance

Revision ID: b752c6d29f63
Revises: 6e3be68b87ae
Create Date: 2020-07-23 09:50:57.663916

"""

# revision identifiers, used by Alembic.
revision = 'b752c6d29f63'
down_revision = '6e3be68b87ae'
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
    op.create_index('ix_pafa_fain_awarding_sub_tier', 'published_award_financial_assistance', ['fain', 'awarding_sub_tier_agency_c'], unique=False)
    op.create_index('ix_pafa_uri_awarding_sub_tier', 'published_award_financial_assistance', ['uri', 'awarding_sub_tier_agency_c'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_place_of_perform_zip_last4'), 'published_award_financial_assistance', ['place_of_perform_zip_last4'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_place_of_perform_county_co'), 'published_award_financial_assistance', ['place_of_perform_county_co'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_place_of_performance_zip5'), 'published_award_financial_assistance', ['place_of_performance_zip5'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_place_of_perfor_state_code'), 'published_award_financial_assistance', ['place_of_perfor_state_code'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_legal_entity_congressional'), 'published_award_financial_assistance', ['legal_entity_congressional'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_legal_entity_county_code'), 'published_award_financial_assistance', ['legal_entity_county_code'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_legal_entity_state_code'), 'published_award_financial_assistance', ['legal_entity_state_code'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_legal_entity_zip5'), 'published_award_financial_assistance', ['legal_entity_zip5'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_legal_entity_zip_last4'), 'published_award_financial_assistance', ['legal_entity_zip_last4'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_award_modification_amendme'), 'published_award_financial_assistance', ['award_modification_amendme'], unique=False)
    op.create_index(op.f('ix_published_award_financial_assistance_business_types'), 'published_award_financial_assistance', ['business_types'], unique=False)
    op.create_index(op.f('ix_pafa_legal_entity_city_name_upper'), 'published_award_financial_assistance', [text('UPPER(legal_entity_city_name)')], unique=False)
    op.create_index(op.f('ix_pafa_legal_entity_state_code_upper'), 'published_award_financial_assistance', [text('UPPER(legal_entity_state_code)')], unique=False)
    op.create_index(op.f('ix_pafa_legal_entity_country_code_upper'), 'published_award_financial_assistance', [text('UPPER(legal_entity_country_code)')], unique=False)
    op.create_index(op.f('ix_pafa_business_funds_indicator_upper'), 'published_award_financial_assistance', [text('UPPER(business_funds_indicator)')], unique=False)
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pafa_business_funds_indicator_upper'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_pafa_legal_entity_country_code_upper'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_pafa_legal_entity_state_code_upper'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_pafa_legal_entity_city_name_upper'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_business_types'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_award_modification_amendme'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_legal_entity_zip_last4'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_legal_entity_zip5'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_legal_entity_state_code'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_legal_entity_county_code'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_legal_entity_congressional'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_place_of_perfor_state_code'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_place_of_performance_zip5'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_place_of_perform_county_co'), table_name='published_award_financial_assistance')
    op.drop_index(op.f('ix_published_award_financial_assistance_place_of_perform_zip_last4'), table_name='published_award_financial_assistance')
    op.drop_index('ix_pafa_uri_awarding_sub_tier', table_name='published_award_financial_assistance')
    op.drop_index('ix_pafa_fain_awarding_sub_tier', table_name='published_award_financial_assistance')
    # ### end Alembic commands ###

