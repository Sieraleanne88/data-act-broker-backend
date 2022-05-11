from tests.unit.dataactcore.factories.staging import FABSFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns
from tests.unit.dataactcore.factories.domain import StateCongressionalFactory

_FILE = 'fabs43_4'


def test_column_headers(database):
    expected_subset = {'row_number', 'place_of_performance_code', 'place_of_performance_congr',
                       'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ Test PrimaryPlaceOfPerformanceCongressionalDistrict exists in the state indicated by the
        PrimaryPlaceOfPerformanceCode or is 90 in a state with multiple districts or when PrimaryPlaceOfPerformanceCode
        is 00*****. Districts that were created under the 2000 census or later are considered valid. This rule is
        ignored when PrimaryPlaceOfPerformanceCode is blank.
    """
    state_congr_1 = StateCongressionalFactory(congressional_district_no='01', state_code='NY', census_year=None)
    state_congr_2 = StateCongressionalFactory(congressional_district_no='02', state_code='NY', census_year=None)
    state_congr_3 = StateCongressionalFactory(congressional_district_no='03', state_code='NY', census_year=2000)

    fabs_1 = FABSFactory(place_of_performance_code='NY12345', place_of_performance_congr='01',
                         correction_delete_indicatr='')
    fabs_2 = FABSFactory(place_of_performance_code='ny*****', place_of_performance_congr='02',
                         correction_delete_indicatr=None)
    fabs_3 = FABSFactory(place_of_performance_code='Ny12345', place_of_performance_congr='03',
                         correction_delete_indicatr='c')
    fabs_4 = FABSFactory(place_of_performance_code='Ny12345', place_of_performance_congr='90',
                         correction_delete_indicatr='C')
    fabs_5 = FABSFactory(place_of_performance_code='00*****', place_of_performance_congr='90',
                         correction_delete_indicatr='')
    fabs_6 = FABSFactory(place_of_performance_code='NY12345', place_of_performance_congr='',
                         correction_delete_indicatr='')
    fabs_7 = FABSFactory(place_of_performance_code='Ny12345', place_of_performance_congr='',
                         correction_delete_indicatr='')
    fabs_8 = FABSFactory(place_of_performance_code='Ny12345', place_of_performance_congr=None,
                         correction_delete_indicatr='')
    # Test ignoring blank/empty string ppop codes
    fabs_9 = FABSFactory(place_of_performance_code='', place_of_performance_congr='03', correction_delete_indicatr='')
    fabs_10 = FABSFactory(place_of_performance_code=None, place_of_performance_congr='03',
                          correction_delete_indicatr='')
    # Ignore correction delete indicator of D
    fabs_11 = FABSFactory(place_of_performance_code='nY12345', place_of_performance_congr='09',
                          correction_delete_indicatr='d')

    errors = number_of_errors(_FILE, database, models=[fabs_1, fabs_2, fabs_3, fabs_4, fabs_5, fabs_6, fabs_7, fabs_8,
                                                       fabs_9, fabs_10, fabs_11, state_congr_1, state_congr_2,
                                                       state_congr_3])
    assert errors == 0


def test_failure(database):
    """ Test failure PrimaryPlaceOfPerformanceCongressionalDistrict exists in the state indicated by the
        PrimaryPlaceOfPerformanceCode or is 90 in a state with multiple districts or when PrimaryPlaceOfPerformanceCode
        is 00*****. Districts that were created under the 2000 census or later are considered valid.
    """
    state_congr_1 = StateCongressionalFactory(congressional_district_no='01', state_code='NY', census_year=None)
    state_congr_2 = StateCongressionalFactory(congressional_district_no='02', state_code='NY', census_year=None)
    state_congr_3 = StateCongressionalFactory(congressional_district_no='01', state_code='PA', census_year=None)
    state_congr_4 = StateCongressionalFactory(congressional_district_no='03', state_code='NJ', census_year=1999)

    fabs_1 = FABSFactory(place_of_performance_code='nY12345', place_of_performance_congr='03',
                         correction_delete_indicatr='')
    fabs_2 = FABSFactory(place_of_performance_code='PA12345', place_of_performance_congr='02',
                         correction_delete_indicatr=None)
    fabs_3 = FABSFactory(place_of_performance_code='PA**345', place_of_performance_congr='90',
                         correction_delete_indicatr='c')
    fabs_4 = FABSFactory(place_of_performance_code='00*****', place_of_performance_congr='01',
                         correction_delete_indicatr='C')
    fabs_5 = FABSFactory(place_of_performance_code='NJ12345', place_of_performance_congr='03',
                         correction_delete_indicatr='')

    errors = number_of_errors(_FILE, database, models=[fabs_1, fabs_2, fabs_3, fabs_4, fabs_5, state_congr_1,
                                                       state_congr_2, state_congr_3, state_congr_4])
    assert errors == 5
