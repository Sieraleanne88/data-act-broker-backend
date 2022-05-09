from tests.unit.dataactcore.factories.domain import OfficeFactory
from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory, PublishedFABSFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs38_detached_award_financial_assistance_4_2'


def test_column_headers(database):
    expected_subset = {'row_number', 'awarding_office_code', 'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success_ignore_null_pafa(database):
    """ Test that empty awarding office codes aren't matching invalid office codes from the base record. """

    office = OfficeFactory(office_code='12345a', financial_assistance_awards_office=True)
    # Base record has no awarding office code, future records don't affect it
    pub_fabs_1 = PublishedFABSFactory(awarding_office_code='', unique_award_key='zyxwv_123', action_date='20181018',
                                      award_modification_amendme='0', is_active=True)
    pub_fabs_2 = PublishedFABSFactory(awarding_office_code='abc', unique_award_key='zyxwv_123', action_date='20181019',
                                      award_modification_amendme='1', is_active=True)
    # Base record has an invalid code but new record has a awarding office entered (ignore this rule)
    pub_fabs_3 = PublishedFABSFactory(awarding_office_code='abc', unique_award_key='abcd_123', action_date='20181019',
                                      award_modification_amendme='0', is_active=True)
    # Base record with a valid office code (case insensitive)
    pub_fabs_4 = PublishedFABSFactory(awarding_office_code='12345A', unique_award_key='1234_abc',
                                      action_date='20181019', award_modification_amendme='0', is_active=True)
    # Earliest record inactive, newer record has valid entry, inactive date matching active doesn't mess it up
    pub_fabs_5 = PublishedFABSFactory(awarding_office_code='abc', unique_award_key='4321_cba', action_date='20181018',
                                      award_modification_amendme='0', is_active=False)
    pub_fabs_6 = PublishedFABSFactory(awarding_office_code='abc', unique_award_key='4321_cba', action_date='20181019',
                                      award_modification_amendme='1', is_active=False)
    pub_fabs_7 = PublishedFABSFactory(awarding_office_code='12345a', unique_award_key='4321_cba',
                                      action_date='20181019', award_modification_amendme='1', is_active=True)

    # New entry for base award with no office code
    det_award_1 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', unique_award_key='zyxwv_123',
                                                          action_date='20181020', award_modification_amendme='2',
                                                          correction_delete_indicatr=None)
    # New entry for base award with invalid code but entry has a awarding office code
    det_award_2 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='abd', unique_award_key='abcd_123',
                                                          action_date='20181020', award_modification_amendme='1',
                                                          correction_delete_indicatr=None)
    # New entry for valid awarding office
    det_award_3 = DetachedAwardFinancialAssistanceFactory(awarding_office_code=None, unique_award_key='1234_abc',
                                                          action_date='20181020', award_modification_amendme='1',
                                                          correction_delete_indicatr=None)
    # Correction to base record (ignore)
    det_award_4 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', unique_award_key='abcd_123',
                                                          action_date='20181019', award_modification_amendme='0',
                                                          correction_delete_indicatr='C')
    # New entry for earliest inactive
    det_award_5 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', unique_award_key='4321_cba',
                                                          action_date='20181020', award_modification_amendme='2',
                                                          correction_delete_indicatr=None)
    errors = number_of_errors(_FILE, database, models=[office, pub_fabs_1, pub_fabs_2, pub_fabs_3, pub_fabs_4,
                                                       pub_fabs_5, pub_fabs_6, pub_fabs_7, det_award_1, det_award_2,
                                                       det_award_3, det_award_4, det_award_5])
    assert errors == 0


def test_failure(database):
    """ Test fail that empty awarding office codes aren't matching invalid office codes from the base record. """

    office_1 = OfficeFactory(office_code='12345a', financial_assistance_awards_office=True)
    office_2 = OfficeFactory(office_code='abcd', financial_assistance_awards_office=False)
    # Invalid code in record
    pub_fabs_1 = PublishedFABSFactory(awarding_office_code='abc', unique_award_key='zyxwv_123', action_date='20181018',
                                      award_modification_amendme='0', is_active=True)
    # Earliest record inactive, newer record has invalid entry
    pub_fabs_2 = PublishedFABSFactory(awarding_office_code='12345a', unique_award_key='4321_cba',
                                      action_date='20181018', award_modification_amendme='0', is_active=False)
    pub_fabs_3 = PublishedFABSFactory(awarding_office_code='abc', unique_award_key='4321_cba', action_date='20181019',
                                      award_modification_amendme='1', is_active=True)
    # Has a valid code but it's not an awarding code
    pub_fabs_4 = PublishedFABSFactory(awarding_office_code='abcd', unique_award_key='123_abc', action_date='20181018',
                                      award_modification_amendme='0', is_active=True)
    # award_modification_amendme number is null
    pub_fabs_5 = PublishedFABSFactory(awarding_office_code='abc', unique_award_key='zyxwv_1234', action_date='20181018',
                                      award_modification_amendme=None, is_active=True)

    # Entry for invalid code in base record
    det_award_1 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', unique_award_key='zyxwv_123',
                                                          action_date='20181020', award_modification_amendme='2',
                                                          correction_delete_indicatr=None)
    # Entry with award_modification_amendme null
    det_award_2 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', unique_award_key='zyxwv_123',
                                                          action_date='20181020', award_modification_amendme=None,
                                                          correction_delete_indicatr=None)
    # New entry for earliest inactive
    det_award_3 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', unique_award_key='4321_cba',
                                                          action_date='20181020', award_modification_amendme='2',
                                                          correction_delete_indicatr=None)
    # New entry for has valid non-awarding code
    det_award_4 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', unique_award_key='123_abc',
                                                          action_date='20181020', award_modification_amendme='2',
                                                          correction_delete_indicatr=None)
    # Entry for award_modification_amendme null in base record
    det_award_5 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', unique_award_key='zyxwv_1234',
                                                          action_date='20181020', award_modification_amendme='2',
                                                          correction_delete_indicatr=None)
    errors = number_of_errors(_FILE, database, models=[office_1, office_2, pub_fabs_1, pub_fabs_2, pub_fabs_3,
                                                       pub_fabs_4, pub_fabs_5, det_award_1, det_award_2, det_award_3,
                                                       det_award_4, det_award_5])
    assert errors == 5
