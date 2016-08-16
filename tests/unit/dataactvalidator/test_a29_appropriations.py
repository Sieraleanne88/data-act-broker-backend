from dataactcore.models.stagingModels import Appropriation
from dataactcore.models.jobModels import Submission
from dataactcore.models.domainModels import SF133
from tests.unit.dataactvalidator.utils import insert_submission, run_sql_rule


_FILE = 'a29_appropriations'
_TAS = 'a29_appropriations_tas'


def test_success(database):
    """ Tests that SF 133 amount sum for lines 1021, 1033 matches Appropriation deobligations_recoveries_r_cpe
        for the specified fiscal year and period """
    tas = "".join([_TAS, "_success"])

    sf_1 = SF133(line=1021, tas=tas, period=1, fiscal_year=2016, amount=1, agency_identifier="sys",
               main_account_code="000", sub_account_code="000")
    sf_2 = SF133(line=1033, tas=tas, period=1, fiscal_year=2016, amount=1, agency_identifier="sys",
               main_account_code="000", sub_account_code="000")
    ap = Appropriation(job_id=1, row_number=1, tas=tas, deobligations_recoveries_r_cpe=2)

    models = [sf_1, sf_2, ap]

    assert run_sql_rule(_FILE, database.stagingDb, models=models) == 0


def test_failure(database):
    """ Tests that SF 133 amount sum for lines 1021, 1033 does not match Appropriation deobligations_recoveries_r_cpe
        for the specified fiscal year and period """
    tas = "".join([_TAS, "_failure"])

    sf_1 = SF133(line=1021, tas=tas, period=1, fiscal_year=2016, amount=1, agency_identifier="sys",
               main_account_code="000", sub_account_code="000")
    sf_2 = SF133(line=1033, tas=tas, period=1, fiscal_year=2016, amount=1, agency_identifier="sys",
               main_account_code="000", sub_account_code="000")
    ap = Appropriation(job_id=1, row_number=1, tas=tas, deobligations_recoveries_r_cpe=1)

    models = [sf_1, sf_2, ap]

    assert run_sql_rule(_FILE, database.stagingDb, models=models) == 1
