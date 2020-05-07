from dataactcore.models.stagingModels import ObjectClassProgramActivity
from dataactcore.models.domainModels import SF133
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns


_FILE = 'b15_object_class_program_activity'
_TAS = 'b15_object_class_program_activity_tas'


def test_column_headers(database):
    expected_subset = {'row_number', 'ussgl480100_undelivered_or_cpe_sum', 'ussgl480100_undelivered_or_fyb_sum',
                       'ussgl480200_undelivered_or_cpe_sum', 'ussgl480200_undelivered_or_fyb_sum',
                       'ussgl488100_upward_adjustm_cpe_sum', 'ussgl488200_upward_adjustm_cpe_sum',
                       'ussgl490100_delivered_orde_cpe_sum', 'ussgl490100_delivered_orde_fyb_sum',
                       'ussgl490200_delivered_orde_cpe_sum', 'ussgl490800_authority_outl_cpe_sum',
                       'ussgl490800_authority_outl_fyb_sum', 'ussgl498100_upward_adjustm_cpe_sum',
                       'ussgl498200_upward_adjustm_cpe_sum', 'expected_value_GTAS SF133 Line 2104',
                       'difference', 'uniqueid_TAS', 'uniqueid_DEFC'}
    actual = set(query_columns(_FILE, database))
    assert (actual & expected_subset) == expected_subset


def test_success(database):
    """ Tests that SF 133 amount sum for line 2104 matches the calculation from Appropriation based on the fields below
        for the specified fiscal year and period and TAS/DEFC combination.
    """
    tas = "".join([_TAS, "_success"])
    tas2 = "".join([_TAS, "_other_tas"])

    # This uses the default submission created in utils for 10/2015 which is period 1 of FY 2016
    sf = SF133(line=2104, tas=tas, period=1, fiscal_year=2016, amount=-15, agency_identifier="sys",
               main_account_code="000", sub_account_code="000", disaster_emergency_fund_code='C')

    op = ObjectClassProgramActivity(job_id=1, row_number=1, tas=tas, by_direct_reimbursable_fun='r',
                                    ussgl480100_undelivered_or_cpe=1, ussgl480100_undelivered_or_fyb=1,
                                    ussgl480200_undelivered_or_cpe=1, ussgl480200_undelivered_or_fyb=1,
                                    ussgl488100_upward_adjustm_cpe=1, ussgl488200_upward_adjustm_cpe=1,
                                    ussgl490100_delivered_orde_cpe=1, ussgl490100_delivered_orde_fyb=1,
                                    ussgl490200_delivered_orde_cpe=1, ussgl490800_authority_outl_cpe=1,
                                    ussgl490800_authority_outl_fyb=1, ussgl498100_upward_adjustm_cpe=1,
                                    ussgl498200_upward_adjustm_cpe=1, disaster_emergency_fund_code='C')
    op2 = ObjectClassProgramActivity(job_id=1, row_number=2, tas=tas, by_direct_reimbursable_fun='r',
                                     ussgl480100_undelivered_or_cpe=2, ussgl480100_undelivered_or_fyb=2,
                                     ussgl480200_undelivered_or_cpe=2, ussgl480200_undelivered_or_fyb=2,
                                     ussgl488100_upward_adjustm_cpe=2, ussgl488200_upward_adjustm_cpe=2,
                                     ussgl490100_delivered_orde_cpe=2, ussgl490100_delivered_orde_fyb=2,
                                     ussgl490200_delivered_orde_cpe=2, ussgl490800_authority_outl_cpe=2,
                                     ussgl490800_authority_outl_fyb=2, ussgl498100_upward_adjustm_cpe=2,
                                     ussgl498200_upward_adjustm_cpe=2, disaster_emergency_fund_code='c')

    # Record for other TAS should not be included in sum
    op3 = ObjectClassProgramActivity(job_id=1, row_number=3, tas=tas2, by_direct_reimbursable_fun='r',
                                     ussgl480100_undelivered_or_cpe=2, ussgl480100_undelivered_or_fyb=2,
                                     ussgl480200_undelivered_or_cpe=2, ussgl480200_undelivered_or_fyb=2,
                                     ussgl488100_upward_adjustm_cpe=2, ussgl488200_upward_adjustm_cpe=2,
                                     ussgl490100_delivered_orde_cpe=2, ussgl490100_delivered_orde_fyb=2,
                                     ussgl490200_delivered_orde_cpe=2, ussgl490800_authority_outl_cpe=2,
                                     ussgl490800_authority_outl_fyb=2, ussgl498100_upward_adjustm_cpe=2,
                                     ussgl498200_upward_adjustm_cpe=2, disaster_emergency_fund_code='C')
    # Record for other DEFC should not be included in sum
    op4 = ObjectClassProgramActivity(job_id=1, row_number=3, tas=tas, by_direct_reimbursable_fun='r',
                                     ussgl480100_undelivered_or_cpe=2, ussgl480100_undelivered_or_fyb=2,
                                     ussgl480200_undelivered_or_cpe=2, ussgl480200_undelivered_or_fyb=2,
                                     ussgl488100_upward_adjustm_cpe=2, ussgl488200_upward_adjustm_cpe=2,
                                     ussgl490100_delivered_orde_cpe=2, ussgl490100_delivered_orde_fyb=2,
                                     ussgl490200_delivered_orde_cpe=2, ussgl490800_authority_outl_cpe=2,
                                     ussgl490800_authority_outl_fyb=2, ussgl498100_upward_adjustm_cpe=2,
                                     ussgl498200_upward_adjustm_cpe=2, disaster_emergency_fund_code='D')

    assert number_of_errors(_FILE, database, models=[sf, op, op2, op3]) == 0


def test_failure(database):
    """ Tests that SF 133 amount sum for line 2104 does not match the calculation from Appropriation based on
        the fields below for the specified fiscal year and period and TAS/DEFC combination.
    """
    tas = "".join([_TAS, "_failure"])

    sf = SF133(line=2104, tas=tas, period=1, fiscal_year=2016, amount=5, agency_identifier="sys",
               main_account_code="000", sub_account_code="000", disaster_emergency_fund_code='D')

    op = ObjectClassProgramActivity(job_id=1, row_number=1, tas=tas, by_direct_reimbursable_fun='r',
                                    ussgl480100_undelivered_or_cpe=1, ussgl480100_undelivered_or_fyb=1,
                                    ussgl480200_undelivered_or_cpe=1, ussgl480200_undelivered_or_fyb=1,
                                    ussgl488100_upward_adjustm_cpe=1, ussgl488200_upward_adjustm_cpe=1,
                                    ussgl490100_delivered_orde_cpe=1, ussgl490100_delivered_orde_fyb=1,
                                    ussgl490200_delivered_orde_cpe=1, ussgl490800_authority_outl_cpe=1,
                                    ussgl490800_authority_outl_fyb=1, ussgl498100_upward_adjustm_cpe=1,
                                    ussgl498200_upward_adjustm_cpe=1, disaster_emergency_fund_code='D')

    op2 = ObjectClassProgramActivity(job_id=1, row_number=2, tas=tas, by_direct_reimbursable_fun='r',
                                     ussgl480100_undelivered_or_cpe=2, ussgl480100_undelivered_or_fyb=2,
                                     ussgl480200_undelivered_or_cpe=2, ussgl480200_undelivered_or_fyb=2,
                                     ussgl488100_upward_adjustm_cpe=2, ussgl488200_upward_adjustm_cpe=2,
                                     ussgl490100_delivered_orde_cpe=2, ussgl490100_delivered_orde_fyb=2,
                                     ussgl490200_delivered_orde_cpe=2, ussgl490800_authority_outl_cpe=2,
                                     ussgl490800_authority_outl_fyb=2, ussgl498100_upward_adjustm_cpe=2,
                                     ussgl498200_upward_adjustm_cpe=2, disaster_emergency_fund_code='D')

    assert number_of_errors(_FILE, database, models=[sf, op, op2]) == 1
