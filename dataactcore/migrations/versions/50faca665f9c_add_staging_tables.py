"""add_staging_tables

Revision ID: 50faca665f9c
Revises: 7833b2378161
Create Date: 2016-08-01 13:52:53.038526

"""

# revision identifiers, used by Alembic.
revision = '50faca665f9c'
down_revision = '7833b2378161'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appropriation',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('appropriation_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('row_number', sa.Integer(), nullable=False),
    sa.Column('adjustments_to_unobligated_cpe', sa.Numeric(), nullable=True),
    sa.Column('agency_identifier', sa.Text(), nullable=True),
    sa.Column('allocation_transfer_agency', sa.Text(), nullable=True),
    sa.Column('availability_type_code', sa.Text(), nullable=True),
    sa.Column('beginning_period_of_availa', sa.Text(), nullable=True),
    sa.Column('borrowing_authority_amount_cpe', sa.Numeric(), nullable=True),
    sa.Column('budget_authority_appropria_cpe', sa.Numeric(), nullable=True),
    sa.Column('budget_authority_available_cpe', sa.Numeric(), nullable=True),
    sa.Column('budget_authority_unobligat_fyb', sa.Numeric(), nullable=True),
    sa.Column('contract_authority_amount_cpe', sa.Numeric(), nullable=True),
    sa.Column('deobligations_recoveries_r_cpe', sa.Numeric(), nullable=True),
    sa.Column('ending_period_of_availabil', sa.Text(), nullable=True),
    sa.Column('gross_outlay_amount_by_tas_cpe', sa.Numeric(), nullable=True),
    sa.Column('main_account_code', sa.Text(), nullable=True),
    sa.Column('obligations_incurred_total_cpe', sa.Numeric(), nullable=True),
    sa.Column('other_budgetary_resources_cpe', sa.Numeric(), nullable=True),
    sa.Column('spending_authority_from_of_cpe', sa.Numeric(), nullable=True),
    sa.Column('status_of_budgetary_resour_cpe', sa.Numeric(), nullable=True),
    sa.Column('sub_account_code', sa.Text(), nullable=True),
    sa.Column('unobligated_balance_cpe', sa.Numeric(), nullable=True),
    sa.Column('tas', sa.Text(), nullable=False),
    sa.Column('is_first_quarter', sa.Boolean(), server_default='False', nullable=False),
    sa.PrimaryKeyConstraint('appropriation_id')
    )
    op.create_index(op.f('ix_appropriation_job_id'), 'appropriation', ['job_id'], unique=False)
    op.create_index(op.f('ix_appropriation_submission_id'), 'appropriation', ['submission_id'], unique=False)
    op.create_index(op.f('ix_appropriation_tas'), 'appropriation', ['tas'], unique=False)
    op.create_table('award_financial',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('award_financial_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('row_number', sa.Integer(), nullable=False),
    sa.Column('agency_identifier', sa.Text(), nullable=True),
    sa.Column('allocation_transfer_agency', sa.Text(), nullable=True),
    sa.Column('availability_type_code', sa.Text(), nullable=True),
    sa.Column('beginning_period_of_availa', sa.Text(), nullable=True),
    sa.Column('by_direct_reimbursable_fun', sa.Text(), nullable=True),
    sa.Column('deobligations_recov_by_awa_cpe', sa.Numeric(), nullable=True),
    sa.Column('ending_period_of_availabil', sa.Text(), nullable=True),
    sa.Column('fain', sa.Text(), nullable=True),
    sa.Column('gross_outlay_amount_by_awa_cpe', sa.Numeric(), nullable=True),
    sa.Column('gross_outlay_amount_by_awa_fyb', sa.Numeric(), nullable=True),
    sa.Column('gross_outlays_delivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('gross_outlays_delivered_or_fyb', sa.Numeric(), nullable=True),
    sa.Column('gross_outlays_undelivered_cpe', sa.Numeric(), nullable=True),
    sa.Column('gross_outlays_undelivered_fyb', sa.Numeric(), nullable=True),
    sa.Column('main_account_code', sa.Text(), nullable=True),
    sa.Column('object_class', sa.Text(), nullable=True),
    sa.Column('obligations_delivered_orde_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligations_delivered_orde_fyb', sa.Numeric(), nullable=True),
    sa.Column('obligations_incurred_byawa_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligations_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligations_undelivered_or_fyb', sa.Numeric(), nullable=True),
    sa.Column('parent_award_id', sa.Text(), nullable=True),
    sa.Column('piid', sa.Text(), nullable=True),
    sa.Column('program_activity_code', sa.Text(), nullable=True),
    sa.Column('program_activity_name', sa.Text(), nullable=True),
    sa.Column('sub_account_code', sa.Text(), nullable=True),
    sa.Column('transaction_obligated_amou', sa.Numeric(), nullable=True),
    sa.Column('uri', sa.Text(), nullable=True),
    sa.Column('ussgl480100_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl480100_undelivered_or_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl480200_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl480200_undelivered_or_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl483100_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl483200_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl487100_downward_adjus_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl487200_downward_adjus_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl488100_upward_adjustm_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl488200_upward_adjustm_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490100_delivered_orde_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490100_delivered_orde_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl490200_delivered_orde_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490800_authority_outl_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490800_authority_outl_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl493100_delivered_orde_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl497100_downward_adjus_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl497200_downward_adjus_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl498100_upward_adjustm_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl498200_upward_adjustm_cpe', sa.Numeric(), nullable=True),
    sa.Column('tas', sa.Text(), nullable=False),
    sa.Column('is_first_quarter', sa.Boolean(), server_default='False', nullable=False),
    sa.PrimaryKeyConstraint('award_financial_id')
    )
    op.create_index(op.f('ix_award_financial_fain'), 'award_financial', ['fain'], unique=False)
    op.create_index(op.f('ix_award_financial_job_id'), 'award_financial', ['job_id'], unique=False)
    op.create_index(op.f('ix_award_financial_piid'), 'award_financial', ['piid'], unique=False)
    op.create_index(op.f('ix_award_financial_submission_id'), 'award_financial', ['submission_id'], unique=False)
    op.create_index('ix_award_financial_tas_oc_pa', 'award_financial', ['tas', 'object_class', 'program_activity_code'], unique=False)
    op.create_index(op.f('ix_award_financial_uri'), 'award_financial', ['uri'], unique=False)
    op.create_table('award_financial_assistance',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('award_financial_assistance_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('row_number', sa.Integer(), nullable=False),
    sa.Column('action_date', sa.Text(), nullable=True),
    sa.Column('action_type', sa.Text(), nullable=True),
    sa.Column('assistance_type', sa.Text(), nullable=True),
    sa.Column('award_description', sa.Text(), nullable=True),
    sa.Column('awardee_or_recipient_legal', sa.Text(), nullable=True),
    sa.Column('awardee_or_recipient_uniqu', sa.Text(), nullable=True),
    sa.Column('awarding_agency_code', sa.Text(), nullable=True),
    sa.Column('awarding_agency_name', sa.Text(), nullable=True),
    sa.Column('awarding_office_code', sa.Text(), nullable=True),
    sa.Column('awarding_office_name', sa.Text(), nullable=True),
    sa.Column('awarding_sub_tier_agency_c', sa.Text(), nullable=True),
    sa.Column('awarding_sub_tier_agency_n', sa.Text(), nullable=True),
    sa.Column('award_modification_amendme', sa.Text(), nullable=True),
    sa.Column('business_funds_indicator', sa.Text(), nullable=True),
    sa.Column('business_types', sa.Text(), nullable=True),
    sa.Column('cfda_number', sa.Text(), nullable=True),
    sa.Column('cfda_title', sa.Text(), nullable=True),
    sa.Column('correction_late_delete_ind', sa.Text(), nullable=True),
    sa.Column('face_value_loan_guarantee', sa.Numeric(), nullable=True),
    sa.Column('fain', sa.Text(), nullable=True),
    sa.Column('federal_action_obligation', sa.Numeric(), nullable=True),
    sa.Column('fiscal_year_and_quarter_co', sa.Text(), nullable=True),
    sa.Column('funding_agency_code', sa.Text(), nullable=True),
    sa.Column('funding_agency_name', sa.Text(), nullable=True),
    sa.Column('funding_office_name', sa.Text(), nullable=True),
    sa.Column('funding_office_code', sa.Text(), nullable=True),
    sa.Column('funding_sub_tier_agency_co', sa.Text(), nullable=True),
    sa.Column('funding_sub_tier_agency_na', sa.Text(), nullable=True),
    sa.Column('legal_entity_address_line1', sa.Text(), nullable=True),
    sa.Column('legal_entity_address_line2', sa.Text(), nullable=True),
    sa.Column('legal_entity_address_line3', sa.Text(), nullable=True),
    sa.Column('legal_entity_city_code', sa.Text(), nullable=True),
    sa.Column('legal_entity_city_name', sa.Text(), nullable=True),
    sa.Column('legal_entity_congressional', sa.Text(), nullable=True),
    sa.Column('legal_entity_country_code', sa.Text(), nullable=True),
    sa.Column('legal_entity_county_code', sa.Text(), nullable=True),
    sa.Column('legal_entity_county_name', sa.Text(), nullable=True),
    sa.Column('legal_entity_foreign_city', sa.Text(), nullable=True),
    sa.Column('legal_entity_foreign_posta', sa.Text(), nullable=True),
    sa.Column('legal_entity_foreign_provi', sa.Text(), nullable=True),
    sa.Column('legal_entity_state_code', sa.Text(), nullable=True),
    sa.Column('legal_entity_state_name', sa.Text(), nullable=True),
    sa.Column('legal_entity_zip5', sa.Text(), nullable=True),
    sa.Column('legal_entity_zip_last4', sa.Text(), nullable=True),
    sa.Column('non_federal_funding_amount', sa.Numeric(), nullable=True),
    sa.Column('original_loan_subsidy_cost', sa.Numeric(), nullable=True),
    sa.Column('period_of_performance_curr', sa.Text(), nullable=True),
    sa.Column('period_of_performance_star', sa.Text(), nullable=True),
    sa.Column('place_of_performance_city', sa.Text(), nullable=True),
    sa.Column('place_of_performance_code', sa.Text(), nullable=True),
    sa.Column('place_of_performance_congr', sa.Text(), nullable=True),
    sa.Column('place_of_perform_country_c', sa.Text(), nullable=True),
    sa.Column('place_of_perform_county_na', sa.Text(), nullable=True),
    sa.Column('place_of_performance_forei', sa.Text(), nullable=True),
    sa.Column('place_of_perform_state_nam', sa.Text(), nullable=True),
    sa.Column('place_of_performance_zip4a', sa.Text(), nullable=True),
    sa.Column('record_type', sa.Integer(), nullable=True),
    sa.Column('sai_number', sa.Text(), nullable=True),
    sa.Column('total_funding_amount', sa.Numeric(), nullable=True),
    sa.Column('uri', sa.Text(), nullable=True),
    sa.Column('is_first_quarter', sa.Boolean(), server_default='False', nullable=False),
    sa.PrimaryKeyConstraint('award_financial_assistance_id')
    )
    op.create_index(op.f('ix_award_financial_assistance_fain'), 'award_financial_assistance', ['fain'], unique=False)
    op.create_index(op.f('ix_award_financial_assistance_job_id'), 'award_financial_assistance', ['job_id'], unique=False)
    op.create_index(op.f('ix_award_financial_assistance_submission_id'), 'award_financial_assistance', ['submission_id'], unique=False)
    op.create_index(op.f('ix_award_financial_assistance_uri'), 'award_financial_assistance', ['uri'], unique=False)
    op.create_table('cgac',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('cgac_id', sa.Integer(), nullable=False),
    sa.Column('cgac_code', sa.Text(), nullable=False),
    sa.Column('agency_name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('cgac_id')
    )
    op.create_index(op.f('ix_cgac_cgac_code'), 'cgac', ['cgac_code'], unique=True)
    op.create_table('object_class',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('object_class_id', sa.Integer(), nullable=False),
    sa.Column('object_class_code', sa.Text(), nullable=False),
    sa.Column('object_class_name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('object_class_id')
    )
    op.create_index(op.f('ix_object_class_object_class_code'), 'object_class', ['object_class_code'], unique=True)
    op.create_table('object_class_program_activity',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('object_class_program_activity_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('row_number', sa.Integer(), nullable=False),
    sa.Column('agency_identifier', sa.Text(), nullable=True),
    sa.Column('allocation_transfer_agency', sa.Text(), nullable=True),
    sa.Column('availability_type_code', sa.Text(), nullable=True),
    sa.Column('beginning_period_of_availa', sa.Text(), nullable=True),
    sa.Column('by_direct_reimbursable_fun', sa.Text(), nullable=True),
    sa.Column('deobligations_recov_by_pro_cpe', sa.Numeric(), nullable=True),
    sa.Column('ending_period_of_availabil', sa.Text(), nullable=True),
    sa.Column('gross_outlay_amount_by_pro_cpe', sa.Numeric(), nullable=True),
    sa.Column('gross_outlay_amount_by_pro_fyb', sa.Numeric(), nullable=True),
    sa.Column('gross_outlays_delivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('gross_outlays_delivered_or_fyb', sa.Numeric(), nullable=True),
    sa.Column('gross_outlays_undelivered_cpe', sa.Numeric(), nullable=True),
    sa.Column('gross_outlays_undelivered_fyb', sa.Numeric(), nullable=True),
    sa.Column('main_account_code', sa.Text(), nullable=True),
    sa.Column('object_class', sa.Text(), nullable=True),
    sa.Column('obligations_delivered_orde_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligations_delivered_orde_fyb', sa.Numeric(), nullable=True),
    sa.Column('obligations_incurred_by_pr_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligations_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('obligations_undelivered_or_fyb', sa.Numeric(), nullable=True),
    sa.Column('program_activity_code', sa.Text(), nullable=True),
    sa.Column('program_activity_name', sa.Text(), nullable=True),
    sa.Column('sub_account_code', sa.Text(), nullable=True),
    sa.Column('ussgl480100_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl480100_undelivered_or_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl480200_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl480200_undelivered_or_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl483100_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl483200_undelivered_or_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl487100_downward_adjus_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl487200_downward_adjus_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl488100_upward_adjustm_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl488200_upward_adjustm_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490100_delivered_orde_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490100_delivered_orde_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl490200_delivered_orde_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490800_authority_outl_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl490800_authority_outl_fyb', sa.Numeric(), nullable=True),
    sa.Column('ussgl493100_delivered_orde_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl497100_downward_adjus_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl497200_downward_adjus_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl498100_upward_adjustm_cpe', sa.Numeric(), nullable=True),
    sa.Column('ussgl498200_upward_adjustm_cpe', sa.Numeric(), nullable=True),
    sa.Column('tas', sa.Text(), nullable=False),
    sa.Column('is_first_quarter', sa.Boolean(), server_default='False', nullable=False),
    sa.PrimaryKeyConstraint('object_class_program_activity_id')
    )
    op.create_index(op.f('ix_object_class_program_activity_job_id'), 'object_class_program_activity', ['job_id'], unique=False)
    op.create_index(op.f('ix_object_class_program_activity_submission_id'), 'object_class_program_activity', ['submission_id'], unique=False)
    op.create_index('ix_oc_pa_tas_oc_pa', 'object_class_program_activity', ['tas', 'object_class', 'program_activity_code'], unique=False)
    op.create_table('program_activity',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('program_activity_id', sa.Integer(), nullable=False),
    sa.Column('budget_year', sa.Text(), nullable=False),
    sa.Column('agency_id', sa.Text(), nullable=False),
    sa.Column('allocation_transfer_id', sa.Text(), nullable=True),
    sa.Column('account_number', sa.Text(), nullable=False),
    sa.Column('program_activity_code', sa.Text(), nullable=False),
    sa.Column('program_activity_name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('program_activity_id')
    )
    op.create_index('ix_pa_tas_pa', 'program_activity', ['budget_year', 'agency_id', 'allocation_transfer_id', 'account_number', 'program_activity_code', 'program_activity_name'], unique=True)
    op.create_table('sf_133',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('sf133_id', sa.Integer(), nullable=False),
    sa.Column('agency_identifier', sa.Text(), nullable=False),
    sa.Column('allocation_transfer_agency', sa.Text(), nullable=True),
    sa.Column('availability_type_code', sa.Text(), nullable=True),
    sa.Column('beginning_period_of_availa', sa.Text(), nullable=True),
    sa.Column('ending_period_of_availabil', sa.Text(), nullable=True),
    sa.Column('main_account_code', sa.Text(), nullable=False),
    sa.Column('sub_account_code', sa.Text(), nullable=False),
    sa.Column('tas', sa.Text(), nullable=False),
    sa.Column('fiscal_year', sa.Text(), nullable=True),
    sa.Column('period', sa.Text(), nullable=True),
    sa.Column('line', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Numeric(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('sf133_id')
    )
    op.create_index('ix_sf_133_tas', 'sf_133', ['tas', 'line'], unique=True)
    op.create_table('tas_lookup',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('tas_id', sa.Integer(), nullable=False),
    sa.Column('allocation_transfer_agency', sa.Text(), nullable=True),
    sa.Column('agency_identifier', sa.Text(), nullable=True),
    sa.Column('beginning_period_of_availability', sa.Text(), nullable=True),
    sa.Column('ending_period_of_availability', sa.Text(), nullable=True),
    sa.Column('availability_type_code', sa.Text(), nullable=True),
    sa.Column('main_account_code', sa.Text(), nullable=True),
    sa.Column('sub_account_code', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('tas_id')
    )
    op.create_index('ix_tas', 'tas_lookup', ['allocation_transfer_agency', 'agency_identifier', 'beginning_period_of_availability', 'ending_period_of_availability', 'availability_type_code', 'main_account_code', 'sub_account_code'], unique=True)
    op.create_index(op.f('ix_tas_lookup_agency_identifier'), 'tas_lookup', ['agency_identifier'], unique=False)
    op.create_index(op.f('ix_tas_lookup_allocation_transfer_agency'), 'tas_lookup', ['allocation_transfer_agency'], unique=False)
    op.create_index(op.f('ix_tas_lookup_availability_type_code'), 'tas_lookup', ['availability_type_code'], unique=False)
    op.create_index(op.f('ix_tas_lookup_beginning_period_of_availability'), 'tas_lookup', ['beginning_period_of_availability'], unique=False)
    op.create_index(op.f('ix_tas_lookup_ending_period_of_availability'), 'tas_lookup', ['ending_period_of_availability'], unique=False)
    op.create_index(op.f('ix_tas_lookup_main_account_code'), 'tas_lookup', ['main_account_code'], unique=False)
    op.create_index(op.f('ix_tas_lookup_sub_account_code'), 'tas_lookup', ['sub_account_code'], unique=False)
    ### end Alembic commands ###


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tas_lookup_sub_account_code'), table_name='tas_lookup')
    op.drop_index(op.f('ix_tas_lookup_main_account_code'), table_name='tas_lookup')
    op.drop_index(op.f('ix_tas_lookup_ending_period_of_availability'), table_name='tas_lookup')
    op.drop_index(op.f('ix_tas_lookup_beginning_period_of_availability'), table_name='tas_lookup')
    op.drop_index(op.f('ix_tas_lookup_availability_type_code'), table_name='tas_lookup')
    op.drop_index(op.f('ix_tas_lookup_allocation_transfer_agency'), table_name='tas_lookup')
    op.drop_index(op.f('ix_tas_lookup_agency_identifier'), table_name='tas_lookup')
    op.drop_index('ix_tas', table_name='tas_lookup')
    op.drop_table('tas_lookup')
    op.drop_index('ix_sf_133_tas', table_name='sf_133')
    op.drop_table('sf_133')
    op.drop_index('ix_pa_tas_pa', table_name='program_activity')
    op.drop_table('program_activity')
    op.drop_index('ix_oc_pa_tas_oc_pa', table_name='object_class_program_activity')
    op.drop_index(op.f('ix_object_class_program_activity_submission_id'), table_name='object_class_program_activity')
    op.drop_index(op.f('ix_object_class_program_activity_job_id'), table_name='object_class_program_activity')
    op.drop_table('object_class_program_activity')
    op.drop_index(op.f('ix_object_class_object_class_code'), table_name='object_class')
    op.drop_table('object_class')
    op.drop_index(op.f('ix_cgac_cgac_code'), table_name='cgac')
    op.drop_table('cgac')
    op.drop_index(op.f('ix_award_financial_assistance_uri'), table_name='award_financial_assistance')
    op.drop_index(op.f('ix_award_financial_assistance_submission_id'), table_name='award_financial_assistance')
    op.drop_index(op.f('ix_award_financial_assistance_job_id'), table_name='award_financial_assistance')
    op.drop_index(op.f('ix_award_financial_assistance_fain'), table_name='award_financial_assistance')
    op.drop_table('award_financial_assistance')
    op.drop_index(op.f('ix_award_financial_uri'), table_name='award_financial')
    op.drop_index('ix_award_financial_tas_oc_pa', table_name='award_financial')
    op.drop_index(op.f('ix_award_financial_submission_id'), table_name='award_financial')
    op.drop_index(op.f('ix_award_financial_piid'), table_name='award_financial')
    op.drop_index(op.f('ix_award_financial_job_id'), table_name='award_financial')
    op.drop_index(op.f('ix_award_financial_fain'), table_name='award_financial')
    op.drop_table('award_financial')
    op.drop_index(op.f('ix_appropriation_tas'), table_name='appropriation')
    op.drop_index(op.f('ix_appropriation_submission_id'), table_name='appropriation')
    op.drop_index(op.f('ix_appropriation_job_id'), table_name='appropriation')
    op.drop_table('appropriation')
    ### end Alembic commands ###

