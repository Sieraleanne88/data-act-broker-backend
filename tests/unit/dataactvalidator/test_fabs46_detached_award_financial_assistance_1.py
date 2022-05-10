from tests.unit.dataactcore.factories.staging import FABSFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs46_detached_award_financial_assistance_1'


def test_column_headers(database):
    expected_subset = {'row_number', 'indirect_federal_sharing', 'assistance_type',
                       'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ Test IndirectCostFederalShareAmount must be blank for non-grants/non-cooperative agreements
        (AssistanceType = 06, 07, 08, 09, 10, or 11).
    """

    fabs_1 = FABSFactory(indirect_federal_sharing=None, assistance_type='09')

    # Doesn't care about other assistance types
    fabs_2 = FABSFactory(indirect_federal_sharing=123, assistance_type='02')
    fabs_3 = FABSFactory(indirect_federal_sharing=456, assistance_type='')

    # Still doesn't trigger when blank for other assistance types
    fabs_4 = FABSFactory(indirect_federal_sharing=None, assistance_type='03')

    # Ignore when CorrectionDeleteIndicator is D
    fabs_5 = FABSFactory(indirect_federal_sharing=123, assistance_type='09', correction_delete_indicatr='d')

    errors = number_of_errors(_FILE, database, models=[fabs_1, fabs_2, fabs_3, fabs_4, fabs_5])
    assert errors == 0


def test_failure(database):
    """ Test failure IndirectCostFederalShareAmount must be blank for non-grants/non-cooperative agreements
        (AssistanceType = 06, 07, 08, 09, 10, or 11).
    """

    fabs_1 = FABSFactory(indirect_federal_sharing=123, assistance_type='11')
    errors = number_of_errors(_FILE, database, models=[fabs_1])
    assert errors == 1
