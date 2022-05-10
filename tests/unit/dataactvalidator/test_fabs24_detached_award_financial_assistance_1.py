from tests.unit.dataactcore.factories.staging import FABSFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs24_detached_award_financial_assistance_1'


def test_column_headers(database):
    expected_subset = {'row_number', 'record_type', 'place_of_perform_country_c',
                       'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ PrimaryPlaceOfPerformanceCountryCode must be blank for record type 3. """
    fabs = FABSFactory(place_of_perform_country_c='USA', record_type=1, correction_delete_indicatr='')
    fabs_2 = FABSFactory(place_of_perform_country_c='uKr', record_type=2, correction_delete_indicatr=None)
    fabs_3 = FABSFactory(place_of_perform_country_c='', record_type=3, correction_delete_indicatr='c')
    fabs_4 = FABSFactory(place_of_perform_country_c=None, record_type=3, correction_delete_indicatr='C')
    # Ignore correction delete indicator of D
    fabs_5 = FABSFactory(place_of_perform_country_c='USA', record_type=3, correction_delete_indicatr='d')

    errors = number_of_errors(_FILE, database, models=[fabs, fabs_2, fabs_3, fabs_4, fabs_5])
    assert errors == 0


def test_failure(database):
    """ PrimaryPlaceOfPerformanceCountryCode must be blank for record type 3. """

    fabs = FABSFactory(place_of_perform_country_c='USA', record_type=3, correction_delete_indicatr='')

    errors = number_of_errors(_FILE, database, models=[fabs])
    assert errors == 1
