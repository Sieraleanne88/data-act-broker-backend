from tests.unit.dataactcore.factories.staging import AwardFinancialFactory, PublishedAwardFinancialFactory
from tests.unit.dataactcore.factories.job import SubmissionFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns, populate_publish_status

from dataactcore.models.lookups import PUBLISH_STATUS_DICT

_FILE = 'c27_award_financial'


def test_column_headers(database):
    expected_subset = {'row_number', 'tas', 'disaster_emergency_fund_code', 'program_activity_code',
                       'program_activity_name', 'object_class', 'by_direct_reimbursable_fun', 'fain', 'uri', 'piid',
                       'parent_award_id', 'gross_outlay_amount_by_awa_cpe', 'uniqueid_TAS',
                       'uniqueid_DisasterEmergencyFundCode', 'uniqueid_ProgramActivityCode',
                       'uniqueid_ProgramActivityCode', 'uniqueid_ProgramActivityName', 'uniqueid_ObjectClass',
                       'uniqueid_ByDirectReimbursableFundingSource', 'uniqueid_FAIN', 'uniqueid_URI', 'uniqueid_PIID',
                       'uniqueid_ParentAwardId'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """
        Test File C GrossOutlayAmountByAward_CPE balance for a TAS, DEFC, program activity code + name, object class
        code, direct/reimbursable flag, and Award ID combination should continue to be reported in subsequent periods
        during the FY, once it has been submitted to DATA Act, unless the most recently reported outlay balance for this
        award breakdown was zero. This only applies to File C outlays, not TOA.
    """
    populate_publish_status(database)
    # Base submission
    sub_1 = SubmissionFactory(submission_id=1, cgac_code='test', reporting_fiscal_year=2020, reporting_fiscal_period=3,
                              frec_code=None, publish_status_id=PUBLISH_STATUS_DICT['published'], d2_submission=False)
    paf_fain = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='aBcD', uri=None,
                                              piid=None, parent_award_id=None, disaster_emergency_fund_code='N',
                                              program_activity_code=None, program_activity_name=None,
                                              object_class=None, by_direct_reimbursable_fun=None,
                                              gross_outlay_amount_by_awa_cpe=5)
    paf_uri = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain=None, uri='eFgH',
                                             piid=None, parent_award_id=None, disaster_emergency_fund_code='n',
                                             program_activity_code=None, program_activity_name=None,
                                             object_class=None, by_direct_reimbursable_fun=None,
                                             gross_outlay_amount_by_awa_cpe=5)
    paf_piid = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain=None, uri=None,
                                              piid='iJkL', parent_award_id=None, disaster_emergency_fund_code='n',
                                              program_activity_code=None, program_activity_name=None,
                                              object_class=None, by_direct_reimbursable_fun=None,
                                              gross_outlay_amount_by_awa_cpe=5)
    paf_paid = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_TAS', fain=None, uri=None,
                                              piid='mNoP', parent_award_id='qRsT', disaster_emergency_fund_code='N',
                                              program_activity_code=None, program_activity_name=None,
                                              object_class=None, by_direct_reimbursable_fun=None,
                                              gross_outlay_amount_by_awa_cpe=5)
    paf_zero = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='xYz', uri=None,
                                              piid=None, parent_award_id=None, disaster_emergency_fund_code='n',
                                              program_activity_code=None, program_activity_name=None,
                                              object_class=None, by_direct_reimbursable_fun=None,
                                              gross_outlay_amount_by_awa_cpe=0)
    paf_null = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='xyZ', uri=None,
                                              piid=None, parent_award_id=None, disaster_emergency_fund_code='n',
                                              program_activity_code=None, program_activity_name=None,
                                              object_class=None, by_direct_reimbursable_fun=None,
                                              gross_outlay_amount_by_awa_cpe=None)
    paf_tas = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='different_tas', fain='hiJK',
                                             uri=None, piid=None, parent_award_id=None,
                                             disaster_emergency_fund_code='n', program_activity_code=None,
                                             program_activity_name=None, object_class=None,
                                             by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    paf_all_9 = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='aBcD',
                                               uri='eFgH', piid='mNoP', parent_award_id='qRsT',
                                               disaster_emergency_fund_code='9', program_activity_code='c',
                                               program_activity_name=None, object_class=None,
                                               by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    paf_pac = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='hiJK',
                                             uri=None, piid=None, parent_award_id=None,
                                             disaster_emergency_fund_code='n', program_activity_code='c',
                                             program_activity_name=None, object_class=None,
                                             by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    paf_pan = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='hiJK',
                                             uri=None, piid=None, parent_award_id=None,
                                             disaster_emergency_fund_code='n', program_activity_code=None,
                                             program_activity_name='n', object_class=None,
                                             by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    paf_obj = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='hiJK',
                                             uri=None, piid=None, parent_award_id=None,
                                             disaster_emergency_fund_code='n', program_activity_code=None,
                                             program_activity_name=None, object_class='c',
                                             by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    paf_dr = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='hiJK',
                                            uri=None, piid=None, parent_award_id=None,
                                            disaster_emergency_fund_code='n', program_activity_code=None,
                                            program_activity_name=None, object_class=None,
                                            by_direct_reimbursable_fun='r', gross_outlay_amount_by_awa_cpe=5)
    database.session.add_all([sub_1, paf_fain, paf_uri, paf_piid, paf_paid, paf_zero, paf_null, paf_tas, paf_all_9,
                              paf_pac, paf_pan, paf_obj, paf_dr])
    database.session.commit()

    # quarterly submission with each of the previous values (one of them is 0 now)
    sub_q = SubmissionFactory(submission_id=2, reporting_fiscal_year=2020, reporting_fiscal_period=6, cgac_code='test',
                              frec_code=None, is_quarter_format=True, d2_submission=False)
    af_fain = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain='abcd', uri=None, piid=None,
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=0)
    af_uri = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain=None, uri='efgh', piid=None,
                                   parent_award_id=None, disaster_emergency_fund_code='n',
                                   program_activity_code=None, program_activity_name=None, object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=3)
    af_piid = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain=None, uri=None, piid='ijkl',
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=7)
    af_paid = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain=None, uri=None, piid='mnop',
                                    parent_award_id='qrst', disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=2)
    af_zero = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain='xyz', uri=None, piid=None,
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=6)
    af_null = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain='xyz', uri=None, piid=None,
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=3)
    af_tas = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='different_tas', fain='hijk', uri=None,
                                   piid=None, parent_award_id=None, disaster_emergency_fund_code='n',
                                   program_activity_code=None, program_activity_name=None, object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=2)
    af_9_match = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain='aBcD', uri='eFgH',
                                       piid='mNoP', parent_award_id='qRsT', disaster_emergency_fund_code='n',
                                       program_activity_code=None, program_activity_name=None, object_class=None,
                                       by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    af_pac = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain='hiJK',
                                   uri=None, piid=None, parent_award_id=None,
                                   disaster_emergency_fund_code='n', program_activity_code='c',
                                   program_activity_name=None, object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=1)
    af_pan = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain='hiJK',
                                   uri=None, piid=None, parent_award_id=None,
                                   disaster_emergency_fund_code='n', program_activity_code=None,
                                   program_activity_name='n', object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=2)
    af_obj = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain='hiJK',
                                   uri=None, piid=None, parent_award_id=None,
                                   disaster_emergency_fund_code='n', program_activity_code=None,
                                   program_activity_name=None, object_class='c',
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=3)
    af_dr = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='test_tas', fain='hiJK',
                                  uri=None, piid=None, parent_award_id=None,
                                  disaster_emergency_fund_code='n', program_activity_code=None,
                                  program_activity_name=None, object_class=None,
                                  by_direct_reimbursable_fun='r', gross_outlay_amount_by_awa_cpe=4)
    # Additional line doesn't mess anything up
    af_bonus = AwardFinancialFactory(submission_id=sub_q.submission_id, tas='something_different')

    errors = number_of_errors(_FILE, database, models=[af_fain, af_uri, af_piid, af_paid, af_zero, af_null, af_tas,
                                                       af_9_match, af_pac, af_pan, af_obj, af_dr, af_bonus],
                              submission=sub_q)
    assert errors == 0

    # period submission with each of the previous values
    sub_p = SubmissionFactory(submission_id=3, reporting_fiscal_year=2020, reporting_fiscal_period=4, cgac_code='test',
                              frec_code=None, is_quarter_format=True, d2_submission=False)
    af_fain = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain='abcd', uri=None, piid=None,
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=9)
    af_uri = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain=None, uri='efgh', piid=None,
                                   parent_award_id=None, disaster_emergency_fund_code='n',
                                   program_activity_code=None, program_activity_name=None, object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=3)
    af_piid = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain=None, uri=None, piid='ijkl',
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=7)
    af_paid = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain=None, uri=None, piid='mnop',
                                    parent_award_id='qrst', disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=2)
    af_zero = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain='xyz', uri=None, piid=None,
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=6)
    af_null = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain='xyz', uri=None, piid=None,
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=3)
    af_tas = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='different_tas', fain='hijk', uri=None,
                                   piid=None, parent_award_id=None, disaster_emergency_fund_code='n',
                                   program_activity_code=None, program_activity_name=None, object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=2)
    # matches the DEFC of 9 with a different DEFC
    af_9_match = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain='aBcD', uri='eFgH',
                                       piid='mNoP', parent_award_id='qRsT', disaster_emergency_fund_code='n',
                                       program_activity_code=None, program_activity_name=None, object_class=None,
                                       by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    af_pac = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain='hiJK',
                                   uri=None, piid=None, parent_award_id=None,
                                   disaster_emergency_fund_code='n', program_activity_code='c',
                                   program_activity_name=None, object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=1)
    af_pan = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain='hiJK',
                                   uri=None, piid=None, parent_award_id=None,
                                   disaster_emergency_fund_code='n', program_activity_code=None,
                                   program_activity_name='n', object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=2)
    af_obj = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain='hiJK',
                                   uri=None, piid=None, parent_award_id=None,
                                   disaster_emergency_fund_code='n', program_activity_code=None,
                                   program_activity_name=None, object_class='c',
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=3)
    af_dr = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='test_tas', fain='hiJK',
                                  uri=None, piid=None, parent_award_id=None,
                                  disaster_emergency_fund_code='n', program_activity_code=None,
                                  program_activity_name=None, object_class=None,
                                  by_direct_reimbursable_fun='r', gross_outlay_amount_by_awa_cpe=4)
    # Additional line doesn't mess anything up
    af_bonus = AwardFinancialFactory(submission_id=sub_p.submission_id, tas='something_different')

    errors = number_of_errors(_FILE, database, models=[af_fain, af_uri, af_piid, af_paid, af_zero, af_null, af_tas,
                                                       af_9_match, af_pac, af_pan, af_obj, af_dr, af_bonus],
                              submission=sub_p)
    assert errors == 0

    # submission missing the values that were 0 and NULL the previous quarter does not throw errors
    sub_4 = SubmissionFactory(submission_id=4, reporting_fiscal_year=2020, reporting_fiscal_period=6, cgac_code='test',
                              frec_code=None, is_quarter_format=True, d2_submission=False)
    af_fain = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain='abcd', uri=None, piid=None,
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=9)
    af_uri = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain=None, uri='efgh', piid=None,
                                   parent_award_id=None, disaster_emergency_fund_code='n',
                                   program_activity_code=None, program_activity_name=None, object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=3)
    af_piid = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain=None, uri=None, piid='ijkl',
                                    parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=7)
    af_paid = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain=None, uri=None, piid='mnop',
                                    parent_award_id='qrst', disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=2)
    af_tas = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='different_tas', fain='hijk', uri=None,
                                   piid=None, parent_award_id=None, disaster_emergency_fund_code='n',
                                   program_activity_code=None, program_activity_name=None, object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=2)
    af_9_match = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain='aBcD', uri='eFgH',
                                       piid='mNoP', parent_award_id='qRsT', disaster_emergency_fund_code='n',
                                       program_activity_code=None, program_activity_name=None, object_class=None,
                                       by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    af_pac = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain='hiJK',
                                   uri=None, piid=None, parent_award_id=None,
                                   disaster_emergency_fund_code='n', program_activity_code='c',
                                   program_activity_name=None, object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=1)
    af_pan = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain='hiJK',
                                   uri=None, piid=None, parent_award_id=None,
                                   disaster_emergency_fund_code='n', program_activity_code=None,
                                   program_activity_name='n', object_class=None,
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=2)
    af_obj = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain='hiJK',
                                   uri=None, piid=None, parent_award_id=None,
                                   disaster_emergency_fund_code='n', program_activity_code=None,
                                   program_activity_name=None, object_class='c',
                                   by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=3)
    af_dr = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain='hiJK',
                                  uri=None, piid=None, parent_award_id=None,
                                  disaster_emergency_fund_code='n', program_activity_code=None,
                                  program_activity_name=None, object_class=None,
                                  by_direct_reimbursable_fun='r', gross_outlay_amount_by_awa_cpe=4)

    errors = number_of_errors(_FILE, database, models=[af_fain, af_uri, af_piid, af_paid, af_tas, af_pac, af_pan,
                                                       af_obj, af_dr, af_9_match],
                              submission=sub_4)
    assert errors == 0

    # submission that doesn't have a "previous period"
    sub_5 = SubmissionFactory(submission_id=5, reporting_fiscal_year=2020, reporting_fiscal_period=5, cgac_code='test',
                              frec_code=None, is_quarter_format=True)

    errors = number_of_errors(_FILE, database, models=[], submission=sub_5)
    assert errors == 0


def test_failure(database):
    """
        Test fail File C GrossOutlayAmountByAward_CPE balance for a TAS, DEFC, program activity code + name, object
        class code, direct/reimbursable flag, and Award ID combination should continue to be reported in subsequent
        periods during the FY, once it has been submitted to DATA Act, unless the most recently reported outlay balance
        for this award breakdown was zero. This only applies to File C outlays, not TOA.
    """
    populate_publish_status(database)
    # Base submission
    sub_1 = SubmissionFactory(submission_id=1, cgac_code='test', reporting_fiscal_year=2020, reporting_fiscal_period=3,
                              frec_code=None, publish_status_id=PUBLISH_STATUS_DICT['published'], d2_submission=False)
    paf_fain = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='abcd', uri=None,
                                              piid=None, parent_award_id=None, disaster_emergency_fund_code='N',
                                              program_activity_code=None, program_activity_name=None,
                                              object_class=None, by_direct_reimbursable_fun=None,
                                              gross_outlay_amount_by_awa_cpe=5)
    paf_defc = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='abcd', uri=None,
                                              piid=None, parent_award_id='testingHere',
                                              disaster_emergency_fund_code='O', program_activity_code=None,
                                              program_activity_name=None, object_class=None,
                                              by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    paf_defc_9 = PublishedAwardFinancialFactory(submission_id=sub_1.submission_id, tas='test_tas', fain='abcd',
                                                uri=None, piid=None, parent_award_id='testingHere',
                                                disaster_emergency_fund_code='9', program_activity_code=None,
                                                program_activity_name=None, object_class=None,
                                                gross_outlay_amount_by_awa_cpe=5)
    database.session.add_all([sub_1, paf_fain, paf_defc, paf_defc_9])
    database.session.commit()

    # submission missing previous period value, missing value of 9 still registers an error
    sub_2 = SubmissionFactory(submission_id=2, reporting_fiscal_year=2020, reporting_fiscal_period=4, cgac_code='test',
                              frec_code=None, is_quarter_format=False, d2_submission=False)

    errors = number_of_errors(_FILE, database, models=[], submission=sub_2)
    assert errors == 3

    # submission with a row that has similar but not exact values (has a uri when the original didn't)
    sub_3 = SubmissionFactory(submission_id=3, reporting_fiscal_year=2020, reporting_fiscal_period=4, cgac_code='test',
                              frec_code=None, is_quarter_format=False, d2_submission=False)
    af_other = AwardFinancialFactory(submission_id=sub_3.submission_id, tas='test_tas', fain='abcd', uri='efgh',
                                     piid=None, parent_award_id=None, disaster_emergency_fund_code='n',
                                     program_activity_code=None, program_activity_name=None, object_class=None,
                                     by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    af_defc = AwardFinancialFactory(submission_id=sub_3.submission_id, tas='test_tas', fain='abcd', uri=None,
                                    piid=None, parent_award_id='testingHere', disaster_emergency_fund_code='O',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    af_defc_9 = AwardFinancialFactory(submission_id=sub_3.submission_id, tas='test_tas', fain='abcd', uri=None,
                                      piid=None, parent_award_id='testingHere', disaster_emergency_fund_code='9',
                                      program_activity_code=None, program_activity_name=None, object_class=None,
                                      by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)

    errors = number_of_errors(_FILE, database, models=[af_other, af_defc, af_defc_9], submission=sub_3)
    assert errors == 2

    # submission with a row that matches but has gross outlay of NULL
    sub_4 = SubmissionFactory(submission_id=4, reporting_fiscal_year=2020, reporting_fiscal_period=4, cgac_code='test',
                              frec_code=None, is_quarter_format=False, d2_submission=False)
    af_null = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain='abcd', uri=None,
                                    piid=None, parent_award_id=None, disaster_emergency_fund_code='n',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=None)
    af_defc_9 = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain='abcd', uri=None,
                                      piid=None, parent_award_id='testingHere', disaster_emergency_fund_code='n',
                                      program_activity_code=None, program_activity_name=None, object_class=None,
                                      by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)
    af_defc = AwardFinancialFactory(submission_id=sub_4.submission_id, tas='test_tas', fain='abcd', uri=None,
                                    piid=None, parent_award_id='testingHere', disaster_emergency_fund_code='o',
                                    program_activity_code=None, program_activity_name=None, object_class=None,
                                    by_direct_reimbursable_fun=None, gross_outlay_amount_by_awa_cpe=5)

    errors = number_of_errors(_FILE, database, models=[af_null, af_defc, af_defc_9], submission=sub_4)
    assert errors == 2
