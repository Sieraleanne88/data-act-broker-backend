import csv
import os
import re
import pytest

from datetime import datetime
from unittest.mock import Mock

from dataactbroker.helpers import generation_helper

from dataactcore.config import CONFIG_BROKER
from dataactcore.models.lookups import JOB_STATUS_DICT, JOB_TYPE_DICT, FILE_TYPE_DICT
from dataactcore.models.stagingModels import DetachedAwardProcurement, PublishedAwardFinancialAssistance
from dataactcore.models.domainModels import SF133, concat_tas_dict, concat_display_tas_dict

from dataactvalidator.validation_handlers import file_generation_manager
from dataactvalidator.validation_handlers.file_generation_manager import FileGenerationManager

from tests.unit.dataactcore.factories.job import JobFactory, FileGenerationFactory, SubmissionFactory
from tests.unit.dataactcore.factories.domain import (TASFactory, SF133Factory, SAMRecipientFactory, CGACFactory,
                                                     FRECFactory)
from tests.unit.dataactcore.factories.staging import (
    AwardFinancialAssistanceFactory, AwardProcurementFactory, DetachedAwardProcurementFactory,
    PublishedAwardFinancialAssistanceFactory)


d1_booleans = ['small_business_competitive', 'city_local_government', 'county_local_government',
               'inter_municipal_local_gove', 'local_government_owned', 'municipality_local_governm',
               'school_district_local_gove', 'township_local_government', 'us_state_government',
               'us_federal_government', 'federal_agency', 'federally_funded_research', 'us_tribal_government',
               'foreign_government', 'community_developed_corpor', 'labor_surplus_area_firm',
               'corporate_entity_not_tax_e', 'corporate_entity_tax_exemp', 'partnership_or_limited_lia',
               'sole_proprietorship', 'small_agricultural_coopera', 'international_organization',
               'us_government_entity', 'emerging_small_business', 'c8a_program_participant',
               'sba_certified_8_a_joint_ve', 'dot_certified_disadvantage', 'self_certified_small_disad',
               'historically_underutilized', 'small_disadvantaged_busine', 'the_ability_one_program',
               'historically_black_college', 'c1862_land_grant_college', 'c1890_land_grant_college',
               'c1994_land_grant_college', 'minority_institution', 'private_university_or_coll', 'school_of_forestry',
               'state_controlled_instituti', 'tribal_college', 'veterinary_college', 'educational_institution',
               'alaskan_native_servicing_i', 'community_development_corp', 'native_hawaiian_servicing',
               'domestic_shelter', 'manufacturer_of_goods', 'hospital_flag', 'veterinary_hospital',
               'hispanic_servicing_institu', 'foundation', 'woman_owned_business', 'minority_owned_business',
               'women_owned_small_business', 'economically_disadvantaged', 'joint_venture_women_owned',
               'joint_venture_economically', 'veteran_owned_business', 'service_disabled_veteran_o', 'contracts',
               'grants', 'receives_contracts_and_gra', 'airport_authority', 'council_of_governments',
               'housing_authorities_public', 'interstate_entity', 'planning_commission', 'port_authority',
               'transit_authority', 'subchapter_s_corporation', 'limited_liability_corporat',
               'foreign_owned_and_located', 'american_indian_owned_busi', 'alaskan_native_owned_corpo',
               'indian_tribe_federally_rec', 'native_hawaiian_owned_busi', 'tribally_owned_business',
               'asian_pacific_american_own', 'black_american_owned_busin', 'hispanic_american_owned_bu',
               'native_american_owned_busi', 'subcontinent_asian_asian_i', 'other_minority_owned_busin',
               'for_profit_organization', 'nonprofit_organization', 'other_not_for_profit_organ', 'us_local_government']


def test_tas_concats():
    # everything
    tas_dict = {
        'allocation_transfer_agency': '097',
        'agency_identifier': '017',
        'beginning_period_of_availa': '2017',
        'ending_period_of_availabil': '2017',
        'availability_type_code': 'D',
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas2_str = concat_tas_dict(tas_dict)
    tas2_dstr = concat_display_tas_dict(tas_dict)
    assert tas2_str == '09701720172017D0001001'
    assert tas2_dstr == '097-017-D-0001-001'

    # everything sans type code
    tas_dict = {
        'allocation_transfer_agency': '097',
        'agency_identifier': '017',
        'beginning_period_of_availa': '2017',
        'ending_period_of_availabil': '2017',
        'availability_type_code': None,
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas2_str = concat_tas_dict(tas_dict)
    tas2_dstr = concat_display_tas_dict(tas_dict)
    assert tas2_str == '09701720172017 0001001'
    assert tas2_dstr == '097-017-2017/2017-0001-001'

    # everything sans ata
    tas_dict = {
        'allocation_transfer_agency': None,
        'agency_identifier': '017',
        'beginning_period_of_availa': '2017',
        'ending_period_of_availabil': '2017',
        'availability_type_code': 'D',
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas2_str = concat_tas_dict(tas_dict)
    tas2_dstr = concat_display_tas_dict(tas_dict)
    assert tas2_str == '00001720172017D0001001'
    assert tas2_dstr == '017-D-0001-001'

    # everything sans aid
    tas_dict = {
        'allocation_transfer_agency': '097',
        'agency_identifier': None,
        'beginning_period_of_availa': '2017',
        'ending_period_of_availabil': '2017',
        'availability_type_code': 'D',
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas2_str = concat_tas_dict(tas_dict)
    tas2_dstr = concat_display_tas_dict(tas_dict)
    assert tas2_str == '09700020172017D0001001'
    assert tas2_dstr == '097-D-0001-001'

    # everything sans periods
    tas_dict = {
        'allocation_transfer_agency': '097',
        'agency_identifier': '017',
        'beginning_period_of_availa': None,
        'ending_period_of_availabil': None,
        'availability_type_code': None,
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas2_str = concat_tas_dict(tas_dict)
    tas2_dstr = concat_display_tas_dict(tas_dict)
    assert tas2_str == '09701700000000 0001001'
    assert tas2_dstr == '097-017-0001-001'

    # everything sans beginning period
    tas_dict = {
        'allocation_transfer_agency': '097',
        'agency_identifier': '017',
        'beginning_period_of_availa': None,
        'ending_period_of_availabil': '2017',
        'availability_type_code': None,
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas2_str = concat_tas_dict(tas_dict)
    tas2_dstr = concat_display_tas_dict(tas_dict)
    assert tas2_str == '09701700002017 0001001'
    assert tas2_dstr == '097-017-2017-0001-001'

    # everything sans codes
    tas_dict = {
        'allocation_transfer_agency': '097',
        'agency_identifier': '017',
        'beginning_period_of_availa': '2017',
        'ending_period_of_availabil': '2017',
        'availability_type_code': 'D',
        'main_account_code': None,
        'sub_account_code': None
    }
    tas2_str = concat_tas_dict(tas_dict)
    tas2_dstr = concat_display_tas_dict(tas_dict)
    assert tas2_str == '09701720172017D0000000'
    assert tas2_dstr == '097-017-D'

    # nothing
    tas_dict = {
        'allocation_transfer_agency': None,
        'agency_identifier': None,
        'beginning_period_of_availa': None,
        'ending_period_of_availabil': None,
        'availability_type_code': None,
        'main_account_code': None,
        'sub_account_code': None
    }
    tas2_str = concat_tas_dict(tas_dict)
    tas2_dstr = concat_display_tas_dict(tas_dict)
    assert tas2_str == '00000000000000 0000000'
    assert tas2_dstr == ''


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_a(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    agency_cgac = '097'
    year = 2017

    tas1_dict = {
        'allocation_transfer_agency': agency_cgac,
        'agency_identifier': '000',
        'beginning_period_of_availa': '2017',
        'ending_period_of_availabil': '2017',
        'availability_type_code': ' ',
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas1_str = concat_tas_dict(tas1_dict)

    tas2_dict = {
        'allocation_transfer_agency': None,
        'agency_identifier': '017',
        'beginning_period_of_availa': '2017',
        'ending_period_of_availabil': '2017',
        'availability_type_code': ' ',
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas2_str = concat_tas_dict(tas2_dict)

    sf1 = SF133Factory(period=6, fiscal_year=year, tas=tas1_str, line=1160, amount='1.00', **tas1_dict)
    sf2 = SF133Factory(period=6, fiscal_year=year, tas=tas1_str, line=1180, amount='2.00', **tas1_dict)
    sf3 = SF133Factory(period=6, fiscal_year=year, tas=tas2_str, line=1000, amount='4.00', **tas2_dict)
    sf4 = SF133Factory(period=6, fiscal_year=year, tas=tas2_str, line=1042, amount='4.00', **tas2_dict)
    sf5 = SF133Factory(period=6, fiscal_year=year, tas=tas2_str, line=1065, amount='4.00', **tas2_dict)
    tas1 = TASFactory(financial_indicator2=' ', **tas1_dict)
    tas2 = TASFactory(financial_indicator2=' ', **tas2_dict)
    job = JobFactory(job_status_id=JOB_STATUS_DICT['running'], job_type_id=JOB_TYPE_DICT['file_upload'],
                     file_type_id=FILE_TYPE_DICT['appropriations'], filename=None, start_date='01/01/2017',
                     end_date='03/31/2017', submission_id=None)
    sess.add_all([sf1, sf2, sf3, sf4, sf5, tas1, tas2, job])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], job=job)
    # providing agency code here as it will be passed via SQS and detached file jobs don't store agency code
    file_gen_manager.generate_file(agency_cgac)

    assert job.filename == os.path.join(CONFIG_BROKER['broker_files'], 'File-A_FY17P06_123456789.csv')

    # check headers
    file_rows = read_file_rows(job.filename)
    assert file_rows[0] == [val[0] for key, val in file_generation_manager.fileA.mapping.items()]

    # check body
    sf1 = sess.query(SF133).filter_by(tas=tas1_str).first()
    sf2 = sess.query(SF133).filter_by(tas=tas2_str).first()
    expected1 = []
    expected2 = []
    sum_cols = [
        'total_budgetary_resources_cpe',
        'budget_authority_appropria_cpe',
        'budget_authority_unobligat_fyb',
        'adjustments_to_unobligated_cpe',
        'other_budgetary_resources_cpe',
        'contract_authority_amount_cpe',
        'borrowing_authority_amount_cpe',
        'spending_authority_from_of_cpe',
        'status_of_budgetary_resour_cpe',
        'obligations_incurred_total_cpe',
        'gross_outlay_amount_by_tas_cpe',
        'unobligated_balance_cpe',
        'deobligations_recoveries_r_cpe'
    ]
    zero_sum_cols = {sum_col: '0' for sum_col in sum_cols}
    expected1_sum_cols = zero_sum_cols.copy()
    expected1_sum_cols['budget_authority_appropria_cpe'] = '3.00'
    expected2_sum_cols = zero_sum_cols.copy()
    expected2_sum_cols['budget_authority_unobligat_fyb'] = '4.00'
    expected2_sum_cols['adjustments_to_unobligated_cpe'] = '4.00'
    for value in file_generation_manager.fileA.db_columns:
        # loop through all values and format date columns
        if value in sf1.__dict__:
            expected1.append(str(sf1.__dict__[value] or ''))
            expected2.append(str(sf2.__dict__[value] or ''))
        elif value in expected1_sum_cols:
            expected1.append(expected1_sum_cols[value])
            expected2.append(expected2_sum_cols[value])

    assert expected1 in file_rows
    assert expected2 in file_rows


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_a_after_2020(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    agency_cgac = '097'
    year = 2021

    tas_dict = {
        'allocation_transfer_agency': agency_cgac,
        'agency_identifier': '000',
        'beginning_period_of_availa': '2021',
        'ending_period_of_availabil': '2021',
        'availability_type_code': ' ',
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas_str = concat_tas_dict(tas_dict)

    sf1 = SF133Factory(period=6, fiscal_year=year, tas=tas_str, line=1042, amount='4.00', **tas_dict)
    sf2 = SF133Factory(period=6, fiscal_year=year, tas=tas_str, line=1065, amount='4.00', **tas_dict)
    tas = TASFactory(financial_indicator2=' ', **tas_dict)
    job = JobFactory(job_status_id=JOB_STATUS_DICT['running'], job_type_id=JOB_TYPE_DICT['file_upload'],
                     file_type_id=FILE_TYPE_DICT['appropriations'], filename=None, start_date='01/01/2021',
                     end_date='03/31/2021', submission_id=None)
    sess.add_all([sf1, sf2, tas, job])
    sess.commit()

    # First job, prior to 2021
    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], job=job)
    # providing agency code here as it will be passed via SQS and detached file jobs don't store agency code
    file_gen_manager.generate_file(agency_cgac)

    assert job.filename == os.path.join(CONFIG_BROKER['broker_files'], 'File-A_FY21P06_123456789.csv')

    # check headers
    file_rows = read_file_rows(job.filename)
    assert file_rows[0] == [val[0] for key, val in file_generation_manager.fileA.mapping.items()]

    # check body
    sf = sess.query(SF133).filter_by(tas=tas_str).first()
    expected = []
    sum_cols = [
        'total_budgetary_resources_cpe',
        'budget_authority_appropria_cpe',
        'budget_authority_unobligat_fyb',
        'adjustments_to_unobligated_cpe',
        'other_budgetary_resources_cpe',
        'contract_authority_amount_cpe',
        'borrowing_authority_amount_cpe',
        'spending_authority_from_of_cpe',
        'status_of_budgetary_resour_cpe',
        'obligations_incurred_total_cpe',
        'gross_outlay_amount_by_tas_cpe',
        'unobligated_balance_cpe',
        'deobligations_recoveries_r_cpe'
    ]
    zero_sum_cols = {sum_col: '0' for sum_col in sum_cols}
    expected_sum_cols = zero_sum_cols.copy()
    expected_sum_cols['adjustments_to_unobligated_cpe'] = '8.00'
    for value in file_generation_manager.fileA.db_columns:
        # loop through all values and format date columns
        if value in sf1.__dict__:
            expected.append(str(sf.__dict__[value] or ''))
        elif value in expected_sum_cols:
            expected.append(expected_sum_cols[value])

    assert expected in file_rows


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_a_null_ata(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    agency_cgac = '097'
    agency_frec = '1137'
    year = 2017

    cgac = CGACFactory(cgac_code=agency_cgac)
    sess.add(cgac)
    sess.commit()

    frec = FRECFactory(frec_code=agency_frec, cgac_id=cgac.cgac_id)
    sess.add(frec)
    sess.commit()

    tas1_dict = {
        'allocation_transfer_agency': None,
        'agency_identifier': '011',
        'beginning_period_of_availa': '2017',
        'ending_period_of_availabil': '2017',
        'availability_type_code': ' ',
        'main_account_code': '0001',
        'sub_account_code': '001'
    }
    tas1_str = concat_tas_dict(tas1_dict)

    tas2_dict = {
        'allocation_transfer_agency': None,
        'agency_identifier': '011',
        'beginning_period_of_availa': '2017',
        'ending_period_of_availabil': '2017',
        'availability_type_code': ' ',
        'main_account_code': '0001',
        'sub_account_code': '002'
    }
    tas2_str = concat_tas_dict(tas2_dict)

    sf1 = SF133Factory(period=6, fiscal_year=year, tas=tas1_str, line=1160, amount='1.00', **tas1_dict)
    sf2 = SF133Factory(period=6, fiscal_year=year, tas=tas1_str, line=1180, amount='2.00', **tas1_dict)
    sf3 = SF133Factory(period=6, fiscal_year=year, tas=tas2_str, line=1000, amount='4.00', **tas2_dict)
    sf4 = SF133Factory(period=6, fiscal_year=year, tas=tas2_str, line=1042, amount='4.00', **tas2_dict)
    sf5 = SF133Factory(period=6, fiscal_year=year, tas=tas2_str, line=1065, amount='4.00', **tas2_dict)
    tas1 = TASFactory(financial_indicator2=' ', fr_entity_type=agency_frec, **tas1_dict)
    tas2 = TASFactory(financial_indicator2=' ', fr_entity_type=agency_frec, **tas2_dict)
    job = JobFactory(job_status_id=JOB_STATUS_DICT['running'], job_type_id=JOB_TYPE_DICT['file_upload'],
                     file_type_id=FILE_TYPE_DICT['appropriations'], filename=None, start_date='01/01/2017',
                     end_date='03/31/2017', submission_id=None)
    sess.add_all([sf1, sf2, sf3, sf4, sf5, tas1, tas2, job])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], job=job)
    # providing agency code here as it will be passed via SQS and detached file jobs don't store agency code
    file_gen_manager.generate_file(agency_cgac)

    assert job.filename == os.path.join(CONFIG_BROKER['broker_files'], 'File-A_FY17P06_123456789.csv')

    # check headers
    file_rows = read_file_rows(job.filename)
    assert file_rows[0] == [val[0] for key, val in file_generation_manager.fileA.mapping.items()]

    # check body
    sf1 = sess.query(SF133).filter_by(tas=tas1_str).first()
    sf2 = sess.query(SF133).filter_by(tas=tas2_str).first()
    expected1 = []
    expected2 = []
    sum_cols = [
        'total_budgetary_resources_cpe',
        'budget_authority_appropria_cpe',
        'budget_authority_unobligat_fyb',
        'adjustments_to_unobligated_cpe',
        'other_budgetary_resources_cpe',
        'contract_authority_amount_cpe',
        'borrowing_authority_amount_cpe',
        'spending_authority_from_of_cpe',
        'status_of_budgetary_resour_cpe',
        'obligations_incurred_total_cpe',
        'gross_outlay_amount_by_tas_cpe',
        'unobligated_balance_cpe',
        'deobligations_recoveries_r_cpe'
    ]
    zero_sum_cols = {sum_col: '0' for sum_col in sum_cols}
    expected1_sum_cols = zero_sum_cols.copy()
    expected1_sum_cols['budget_authority_appropria_cpe'] = '3.00'
    expected2_sum_cols = zero_sum_cols.copy()
    expected2_sum_cols['budget_authority_unobligat_fyb'] = '4.00'
    expected2_sum_cols['adjustments_to_unobligated_cpe'] = '4.00'
    for value in file_generation_manager.fileA.db_columns:
        # loop through all values and format date columns
        if value in sf1.__dict__:
            expected1.append(str(sf1.__dict__[value] or ''))
            expected2.append(str(sf2.__dict__[value] or ''))
        elif value in expected1_sum_cols:
            expected1.append(expected1_sum_cols[value])
            expected2.append(expected2_sum_cols[value])

    assert expected1 in file_rows
    assert expected2 in file_rows


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_sub_d1(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    dap_model = DetachedAwardProcurementFactory
    dap_1 = dap_model(awarding_agency_code='123', action_date='20170101', detached_award_proc_unique='unique1')
    dap_2 = dap_model(awarding_agency_code='123', action_date='20170131', detached_award_proc_unique='unique2')
    dap_3 = dap_model(awarding_agency_code='123', action_date='20170201', detached_award_proc_unique='unique3')
    dap_4 = dap_model(awarding_agency_code='123', action_date='20161231', detached_award_proc_unique='unique4')
    dap_5 = dap_model(awarding_agency_code='234', action_date='20170115', detached_award_proc_unique='unique5')
    file_gen = FileGenerationFactory(request_date=datetime.now().date(), start_date='01/01/2017', end_date='01/31/2017',
                                     file_type='D1', agency_code='123', agency_type='awarding', is_cached_file=False,
                                     file_path=None, file_format='csv')
    sub = SubmissionFactory(submission_id=4, reporting_fiscal_year='2022', reporting_fiscal_period='4')
    job = JobFactory(submission_id=4, file_type_id=FILE_TYPE_DICT['award_procurement'])
    sess.add_all([dap_1, dap_2, dap_3, dap_4, dap_5, file_gen, sub, job])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], file_generation=file_gen, job=job)
    file_gen_manager.generate_file()

    assert file_gen.file_path == os.path.join(CONFIG_BROKER['broker_files'],
                                              'SubID-4_File-D1_FY22P04_20170101_20170131_awarding_123456789.csv')


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_sub_d2(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    dap_model = DetachedAwardProcurementFactory
    dap_1 = dap_model(awarding_agency_code='123', action_date='20170101', detached_award_proc_unique='unique1')
    dap_2 = dap_model(awarding_agency_code='123', action_date='20170131', detached_award_proc_unique='unique2')
    dap_3 = dap_model(awarding_agency_code='123', action_date='20170201', detached_award_proc_unique='unique3')
    dap_4 = dap_model(awarding_agency_code='123', action_date='20161231', detached_award_proc_unique='unique4')
    dap_5 = dap_model(awarding_agency_code='234', action_date='20170115', detached_award_proc_unique='unique5')
    file_gen = FileGenerationFactory(request_date=datetime.now().date(), start_date='01/01/2017', end_date='01/31/2017',
                                     file_type='D1', agency_code='123', agency_type='funding', is_cached_file=False,
                                     file_path=None, file_format='txt')
    sub = SubmissionFactory(submission_id=4, reporting_fiscal_year='2022', reporting_fiscal_period='4')
    job = JobFactory(submission_id=4, file_type_id=FILE_TYPE_DICT['award'])
    sess.add_all([dap_1, dap_2, dap_3, dap_4, dap_5, file_gen, sub, job])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], file_generation=file_gen, job=job)
    file_gen_manager.generate_file()

    assert file_gen.file_path == os.path.join(CONFIG_BROKER['broker_files'],
                                              'SubID-4_File-D2_FY22P04_20170101_20170131_funding_123456789.txt')


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_awarding_d1(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    dap_model = DetachedAwardProcurementFactory
    dap_1 = dap_model(awarding_agency_code='123', action_date='20170101', detached_award_proc_unique='unique1')
    dap_2 = dap_model(awarding_agency_code='123', action_date='20170131', detached_award_proc_unique='unique2')
    dap_3 = dap_model(awarding_agency_code='123', action_date='20170201', detached_award_proc_unique='unique3')
    dap_4 = dap_model(awarding_agency_code='123', action_date='20161231', detached_award_proc_unique='unique4')
    dap_5 = dap_model(awarding_agency_code='234', action_date='20170115', detached_award_proc_unique='unique5')
    file_gen = FileGenerationFactory(request_date=datetime.now().date(), start_date='01/01/2017', end_date='01/31/2017',
                                     file_type='D1', agency_code='123', agency_type='awarding', is_cached_file=True,
                                     file_path=None, file_format='csv')
    sess.add_all([dap_1, dap_2, dap_3, dap_4, dap_5, file_gen])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], file_generation=file_gen)
    file_gen_manager.generate_file()

    assert file_gen.file_path == os.path.join(CONFIG_BROKER['broker_files'],
                                              'File-D1_20170101_20170131_awarding_123456789.csv')

    # check headers
    file_rows = read_file_rows(file_gen.file_path)
    assert file_rows[0] == [val[0] for key, val in file_generation_manager.fileD1.mapping.items()]

    # check body
    dap_one = sess.query(DetachedAwardProcurement).filter_by(detached_award_proc_unique='unique1').first()
    dap_two = sess.query(DetachedAwardProcurement).filter_by(detached_award_proc_unique='unique2').first()
    expected1, expected2 = [], []
    for value in file_generation_manager.fileD1.db_columns:
        # loop through all values and format date columns
        if value in ['period_of_performance_star', 'period_of_performance_curr', 'period_of_perf_potential_e',
                     'ordering_period_end_date', 'action_date', 'last_modified', 'solicitation_date']:
            expected1.append(re.sub(r"[-]", r"", str(dap_one.__dict__[value]))[0:8])
            expected2.append(re.sub(r"[-]", r"", str(dap_two.__dict__[value]))[0:8])
        elif value in d1_booleans:
            expected1.append(str(dap_one.__dict__[value])[0:1].lower() if dap_one.__dict__[value] is not None else None)
            expected2.append(str(dap_two.__dict__[value])[0:1].lower() if dap_two.__dict__[value] is not None else None)
        else:
            expected1.append(str(dap_one.__dict__[value]))
            expected2.append(str(dap_two.__dict__[value]))

    assert expected1 in file_rows
    assert expected2 in file_rows


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_awarding_d1_alternate_headers(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    dap_model = DetachedAwardProcurementFactory
    dap_1 = dap_model(awarding_agency_code='123', action_date='20170101', detached_award_proc_unique='unique1')
    dap_2 = dap_model(awarding_agency_code='123', action_date='20170131', detached_award_proc_unique='unique2')
    dap_3 = dap_model(awarding_agency_code='123', action_date='20170201', detached_award_proc_unique='unique3')
    dap_4 = dap_model(awarding_agency_code='123', action_date='20161231', detached_award_proc_unique='unique4')
    dap_5 = dap_model(awarding_agency_code='234', action_date='20170115', detached_award_proc_unique='unique5')
    file_gen = FileGenerationFactory(request_date=datetime.now().date(), start_date='01/01/2017', end_date='01/31/2017',
                                     file_type='D1', agency_code='123', agency_type='awarding', is_cached_file=True,
                                     file_path=None, file_format='csv', element_numbers=True)
    sess.add_all([dap_1, dap_2, dap_3, dap_4, dap_5, file_gen])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], file_generation=file_gen)
    file_gen_manager.generate_file()

    assert file_gen.file_path == os.path.join(CONFIG_BROKER['broker_files'],
                                              'File-D1_20170101_20170131_awarding_123456789.csv')

    # check headers
    file_rows = read_file_rows(file_gen.file_path)
    assert file_rows[0] == [val[1] for key, val in file_generation_manager.fileD1.mapping.items()]

    # check body
    dap_one = sess.query(DetachedAwardProcurement).filter_by(detached_award_proc_unique='unique1').first()
    dap_two = sess.query(DetachedAwardProcurement).filter_by(detached_award_proc_unique='unique2').first()
    expected1, expected2 = [], []
    for value in file_generation_manager.fileD1.db_columns:
        # loop through all values and format date columns
        if value in ['period_of_performance_star', 'period_of_performance_curr', 'period_of_perf_potential_e',
                     'ordering_period_end_date', 'action_date', 'last_modified', 'solicitation_date']:
            expected1.append(re.sub(r"[-]", r"", str(dap_one.__dict__[value]))[0:8])
            expected2.append(re.sub(r"[-]", r"", str(dap_two.__dict__[value]))[0:8])
        elif value in d1_booleans:
            expected1.append(str(dap_one.__dict__[value])[0:1].lower() if dap_one.__dict__[value] is not None else None)
            expected2.append(str(dap_two.__dict__[value])[0:1].lower() if dap_two.__dict__[value] is not None else None)
        else:
            expected1.append(str(dap_one.__dict__[value]))
            expected2.append(str(dap_two.__dict__[value]))

    assert expected1 in file_rows
    assert expected2 in file_rows


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_funding_d1(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    dap_model = DetachedAwardProcurementFactory
    dap_1 = dap_model(funding_agency_code='123', action_date='20170101', detached_award_proc_unique='unique1')
    dap_2 = dap_model(funding_agency_code='123', action_date='20170131', detached_award_proc_unique='unique2')
    dap_3 = dap_model(funding_agency_code='123', action_date='20170201', detached_award_proc_unique='unique3')
    dap_4 = dap_model(funding_agency_code='123', action_date='20161231', detached_award_proc_unique='unique4')
    dap_5 = dap_model(funding_agency_code='234', action_date='20170115', detached_award_proc_unique='unique5')
    file_gen = FileGenerationFactory(request_date=datetime.now().date(), start_date='01/01/2017', end_date='01/31/2017',
                                     file_type='D1', agency_code='123', agency_type='funding', is_cached_file=True,
                                     file_path=None, file_format='csv')
    sess.add_all([dap_1, dap_2, dap_3, dap_4, dap_5, file_gen])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], file_generation=file_gen)
    file_gen_manager.generate_file()

    assert file_gen.file_path == os.path.join(CONFIG_BROKER['broker_files'],
                                              'File-D1_20170101_20170131_funding_123456789.csv')

    # check headers
    file_rows = read_file_rows(file_gen.file_path)
    assert file_rows[0] == [val[0] for key, val in file_generation_manager.fileD1.mapping.items()]

    # check body
    dap_one = sess.query(DetachedAwardProcurement).filter_by(detached_award_proc_unique='unique1').first()
    dap_two = sess.query(DetachedAwardProcurement).filter_by(detached_award_proc_unique='unique2').first()
    expected1, expected2 = [], []
    for value in file_generation_manager.fileD1.db_columns:
        # loop through all values and format date columns
        if value in ['period_of_performance_star', 'period_of_performance_curr', 'period_of_perf_potential_e',
                     'ordering_period_end_date', 'action_date', 'last_modified', 'solicitation_date']:
            expected1.append(re.sub(r"[-]", r"", str(dap_one.__dict__[value]))[0:8])
            expected2.append(re.sub(r"[-]", r"", str(dap_two.__dict__[value]))[0:8])
        elif value in d1_booleans:
            expected1.append(str(dap_one.__dict__[value])[0:1].lower() if dap_one.__dict__[value] is not None else None)
            expected2.append(str(dap_two.__dict__[value])[0:1].lower() if dap_two.__dict__[value] is not None else None)
        else:
            expected1.append(str(dap_one.__dict__[value]))
            expected2.append(str(dap_two.__dict__[value]))

    assert expected1 in file_rows
    assert expected2 in file_rows


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_awarding_d2(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    pafa = PublishedAwardFinancialAssistanceFactory
    pafa_1 = pafa(awarding_agency_code='123', action_date='20170101', afa_generated_unique='unique1', is_active=True)
    pafa_2 = pafa(awarding_agency_code='123', action_date='20170131', afa_generated_unique='unique2', is_active=True)
    pafa_3 = pafa(awarding_agency_code='123', action_date='20161231', afa_generated_unique='unique3', is_active=True)
    pafa_4 = pafa(awarding_agency_code='123', action_date='20170201', afa_generated_unique='unique4', is_active=True)
    pafa_5 = pafa(awarding_agency_code='123', action_date='20170115', afa_generated_unique='unique5', is_active=False)
    pafa_6 = pafa(awarding_agency_code='234', action_date='20170115', afa_generated_unique='unique6', is_active=True)
    file_gen = FileGenerationFactory(request_date=datetime.now().date(), start_date='01/01/2017', end_date='01/31/2017',
                                     file_type='D2', agency_code='123', agency_type='awarding', is_cached_file=True,
                                     file_path=None, file_format='csv')
    sess.add_all([pafa_1, pafa_2, pafa_3, pafa_4, pafa_5, pafa_6, file_gen])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], file_generation=file_gen)
    file_gen_manager.generate_file()

    assert file_gen.file_path == os.path.join(CONFIG_BROKER['broker_files'],
                                              'File-D2_20170101_20170131_awarding_123456789.csv')

    # check headers
    file_rows = read_file_rows(file_gen.file_path)
    assert file_rows[0] == [val[0] for key, val in file_generation_manager.fileD2.mapping.items()]

    # check body
    pafa1 = sess.query(PublishedAwardFinancialAssistance).filter_by(afa_generated_unique='unique1').first()
    pafa2 = sess.query(PublishedAwardFinancialAssistance).filter_by(afa_generated_unique='unique2').first()
    expected1, expected2 = [], []
    for value in file_generation_manager.fileD2.db_columns:
        # loop through all values and format date columns
        if value in ['period_of_performance_star', 'period_of_performance_curr', 'modified_at', 'action_date']:
            expected1.append(re.sub(r"[-]", r"", str(pafa1.__dict__[value]))[0:8])
            expected2.append(re.sub(r"[-]", r"", str(pafa2.__dict__[value]))[0:8])
        else:
            expected1.append(str(pafa1.__dict__[value] or ''))
            expected2.append(str(pafa2.__dict__[value] or ''))

    assert expected1 in file_rows
    assert expected2 in file_rows


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_funding_d2(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    pafa = PublishedAwardFinancialAssistanceFactory
    pafa_1 = pafa(funding_agency_code='123', action_date='20170101', afa_generated_unique='unique1', is_active=True)
    pafa_2 = pafa(funding_agency_code='123', action_date='20170131', afa_generated_unique='unique2', is_active=True)
    pafa_3 = pafa(funding_agency_code='123', action_date='20161231', afa_generated_unique='unique3', is_active=True)
    pafa_4 = pafa(funding_agency_code='123', action_date='20170201', afa_generated_unique='unique4', is_active=True)
    pafa_5 = pafa(funding_agency_code='123', action_date='20170115', afa_generated_unique='unique5', is_active=False)
    pafa_6 = pafa(funding_agency_code='234', action_date='20170115', afa_generated_unique='unique6', is_active=True)
    file_gen = FileGenerationFactory(request_date=datetime.now().date(), start_date='01/01/2017', end_date='01/31/2017',
                                     file_type='D2', agency_code='123', agency_type='funding', is_cached_file=True,
                                     file_path=None, file_format='csv')
    sess.add_all([pafa_1, pafa_2, pafa_3, pafa_4, pafa_5, pafa_6, file_gen])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], file_generation=file_gen)
    file_gen_manager.generate_file()

    assert file_gen.file_path == os.path.join(CONFIG_BROKER['broker_files'],
                                              'File-D2_20170101_20170131_funding_123456789.csv')

    # check headers
    file_rows = read_file_rows(file_gen.file_path)
    assert file_rows[0] == [val[0] for key, val in file_generation_manager.fileD2.mapping.items()]

    # check body
    pafa1 = sess.query(PublishedAwardFinancialAssistance).filter_by(afa_generated_unique='unique1').first()
    pafa2 = sess.query(PublishedAwardFinancialAssistance).filter_by(afa_generated_unique='unique2').first()
    expected1, expected2 = [], []
    for value in file_generation_manager.fileD2.db_columns:
        # loop through all values and format date columns
        if value in ['period_of_performance_star', 'period_of_performance_curr', 'modified_at', 'action_date']:
            expected1.append(re.sub(r"[-]", r"", str(pafa1.__dict__[value]))[0:8])
            expected2.append(re.sub(r"[-]", r"", str(pafa2.__dict__[value]))[0:8])
        else:
            expected1.append(str(pafa1.__dict__[value] or ''))
            expected2.append(str(pafa2.__dict__[value] or ''))

    assert expected1 in file_rows
    assert expected2 in file_rows


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_txt_d1(database, monkeypatch):
    sess = database.session
    monkeypatch.setattr(file_generation_manager, 'get_timestamp', Mock(return_value='123456789'))

    dap_model = DetachedAwardProcurementFactory
    dap_1 = dap_model(awarding_agency_code='123', action_date='20170101', detached_award_proc_unique='unique1')
    dap_2 = dap_model(awarding_agency_code='123', action_date='20170131', detached_award_proc_unique='unique2')
    dap_3 = dap_model(awarding_agency_code='123', action_date='20170201', detached_award_proc_unique='unique3')
    dap_4 = dap_model(awarding_agency_code='123', action_date='20161231', detached_award_proc_unique='unique4')
    dap_5 = dap_model(awarding_agency_code='234', action_date='20170115', detached_award_proc_unique='unique5')
    file_gen = FileGenerationFactory(request_date=datetime.now().date(), start_date='01/01/2017', end_date='01/31/2017',
                                     file_type='D1', agency_code='123', agency_type='awarding', is_cached_file=True,
                                     file_path=None, file_format='txt')
    sess.add_all([dap_1, dap_2, dap_3, dap_4, dap_5, file_gen])
    sess.commit()

    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], file_generation=file_gen)
    file_gen_manager.generate_file()

    assert file_gen.file_path == os.path.join(CONFIG_BROKER['broker_files'],
                                              'File-D1_20170101_20170131_awarding_123456789.txt')

    # check headers
    file_rows = read_file_rows(file_gen.file_path, delimiter='|')
    assert file_rows[0] == [val[0] for key, val in file_generation_manager.fileD1.mapping.items()]

    # check body
    dap_one = sess.query(DetachedAwardProcurement).filter_by(detached_award_proc_unique='unique1').first()
    dap_two = sess.query(DetachedAwardProcurement).filter_by(detached_award_proc_unique='unique2').first()
    expected1, expected2 = [], []
    for value in file_generation_manager.fileD1.db_columns:
        # loop through all values and format date columns
        if value in ['period_of_performance_star', 'period_of_performance_curr', 'period_of_perf_potential_e',
                     'ordering_period_end_date', 'action_date', 'last_modified', 'solicitation_date']:
            expected1.append(re.sub(r"[-]", r"", str(dap_one.__dict__[value]))[0:8])
            expected2.append(re.sub(r"[-]", r"", str(dap_two.__dict__[value]))[0:8])
        elif value in d1_booleans:
            expected1.append(str(dap_one.__dict__[value])[0:1].lower() if dap_one.__dict__[value] is not None else None)
            expected2.append(str(dap_two.__dict__[value])[0:1].lower() if dap_two.__dict__[value] is not None else None)
        else:
            expected1.append(str(dap_one.__dict__[value]))
            expected2.append(str(dap_two.__dict__[value]))

    assert expected1 in file_rows
    assert expected2 in file_rows


@pytest.mark.usefixtures("job_constants", "broker_files_tmp_dir")
def test_generate_file_updates_jobs(monkeypatch, database):
    sess = database.session
    job1 = JobFactory(job_status_id=JOB_STATUS_DICT['running'], job_type_id=JOB_TYPE_DICT['file_upload'],
                      file_type_id=FILE_TYPE_DICT['award_procurement'], filename=None, original_filename=None,
                      start_date='01/01/2017', end_date='01/31/2017')
    job2 = JobFactory(job_status_id=JOB_STATUS_DICT['running'], job_type_id=JOB_TYPE_DICT['file_upload'],
                      file_type_id=FILE_TYPE_DICT['award_procurement'], filename=None, original_filename=None,
                      start_date='01/01/2017', end_date='01/31/2017')
    job3 = JobFactory(job_status_id=JOB_STATUS_DICT['running'], job_type_id=JOB_TYPE_DICT['file_upload'],
                      file_type_id=FILE_TYPE_DICT['award_procurement'], filename=None, original_filename=None,
                      start_date='01/01/2017', end_date='01/31/2017')
    file_gen = FileGenerationFactory(request_date=datetime.now().date(), start_date='01/01/2017', end_date='01/31/2017',
                                     file_type='D1', agency_code='123', agency_type='awarding', is_cached_file=True,
                                     file_path=None, file_format='csv')
    sess.add_all([job1, job2, job3, file_gen])
    sess.commit()
    job1.file_generation_id = file_gen.file_generation_id
    job2.file_generation_id = file_gen.file_generation_id
    job3.file_generation_id = file_gen.file_generation_id
    sess.commit()

    monkeypatch.setattr(generation_helper, 'g', Mock(return_value={'is_local': CONFIG_BROKER['local']}))
    file_gen_manager = FileGenerationManager(sess, CONFIG_BROKER['local'], file_generation=file_gen)
    file_gen_manager.generate_file()
    sess.refresh(file_gen)

    original_filename = file_gen.file_path.split('/')[-1]

    assert job1.job_status_id == JOB_STATUS_DICT['finished']
    assert job1.original_filename == original_filename
    assert job1.filename == '{}{}'.format(
        CONFIG_BROKER['broker_files'] if CONFIG_BROKER['local'] else job1.submission_id + '/', original_filename)

    assert job2.job_status_id == JOB_STATUS_DICT['finished']
    assert job2.original_filename == original_filename
    assert job2.filename == '{}{}'.format(
        CONFIG_BROKER['broker_files'] if CONFIG_BROKER['local'] else job2.submission_id + '/', original_filename)

    assert job3.job_status_id == JOB_STATUS_DICT['finished']
    assert job3.original_filename == original_filename
    assert job3.filename == '{}{}'.format(
        CONFIG_BROKER['broker_files'] if CONFIG_BROKER['local'] else job3.submission_id + '/', original_filename)


@pytest.mark.usefixtures("job_constants")
def test_generate_e_file(mock_broker_config_paths, database):
    """ Verify that generate_e_file makes an appropriate query (matching both D1 and D2 entries) and creates
        a file matching the expected recipient
    """
    # Generate several file D1 entries, largely with the same submission_id, and with two overlapping UEI. Generate
    # several D2 entries with the same submission_id as well
    sess = database.session
    sub = SubmissionFactory()
    sub_2 = SubmissionFactory()
    sess.add_all([sub, sub_2])
    sess.commit()

    file_path = str(mock_broker_config_paths['broker_files'].join('e_test1'))
    job = JobFactory(job_status_id=JOB_STATUS_DICT['running'], job_type_id=JOB_TYPE_DICT['file_upload'],
                     file_type_id=FILE_TYPE_DICT['executive_compensation'], filename=file_path,
                     original_filename='e_test1', submission_id=sub.submission_id)
    database.session.add(job)
    database.session.commit()

    model = AwardProcurementFactory(submission_id=sub.submission_id)
    aps = [AwardProcurementFactory(submission_id=sub.submission_id) for _ in range(4)]
    afas = [AwardFinancialAssistanceFactory(submission_id=sub.submission_id) for _ in range(5)]
    same_uei = AwardProcurementFactory(
        submission_id=sub.submission_id,
        awardee_or_recipient_uei=model.awardee_or_recipient_uei)
    unrelated = AwardProcurementFactory(submission_id=sub_2.submission_id)
    uei_list = [SAMRecipientFactory(uei=model.awardee_or_recipient_uei)]
    uei_list.extend([SAMRecipientFactory(uei=ap.awardee_or_recipient_uei) for ap in aps])
    uei_list.extend([SAMRecipientFactory(uei=afa.awardee_or_recipient_uei) for afa in afas])
    sess.add_all(aps + afas + uei_list + [model, same_uei, unrelated])
    sess.commit()

    file_gen_manager = FileGenerationManager(database.session, CONFIG_BROKER['local'], job=job)
    file_gen_manager.generate_file()

    # check headers
    file_rows = read_file_rows(file_path)
    assert file_rows[0] == ['AwardeeOrRecipientUEI', 'AwardeeOrRecipientLegalEntityName', 'UltimateParentUEI',
                            'UltimateParentLegalEntityName', 'HighCompOfficer1FullName', 'HighCompOfficer1Amount',
                            'HighCompOfficer2FullName', 'HighCompOfficer2Amount', 'HighCompOfficer3FullName',
                            'HighCompOfficer3Amount', 'HighCompOfficer4FullName', 'HighCompOfficer4Amount',
                            'HighCompOfficer5FullName', 'HighCompOfficer5Amount']

    # Check listed UEI
    expected = [[uei.uei, uei.legal_business_name, uei.ultimate_parent_uei, uei.ultimate_parent_legal_enti,
                 uei.high_comp_officer1_full_na, uei.high_comp_officer1_amount, uei.high_comp_officer2_full_na,
                 uei.high_comp_officer2_amount, uei.high_comp_officer3_full_na, uei.high_comp_officer3_amount,
                 uei.high_comp_officer4_full_na, uei.high_comp_officer4_amount, uei.high_comp_officer5_full_na,
                 uei.high_comp_officer5_amount]
                for uei in uei_list]
    received = [file_row for file_row in file_rows[1:]]
    assert sorted(received) == list(sorted(expected))


def read_file_rows(file_path, delimiter=','):
    """ Helper to read the file rows in the provided file. """
    assert os.path.isfile(file_path)

    with open(file_path) as f:
        return [row for row in csv.reader(f, delimiter=delimiter)]
