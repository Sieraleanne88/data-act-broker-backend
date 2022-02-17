-- BudgetAuthorityUnobligatedBalanceBroughtForward_FYB should have an amount populated for the reporting period
-- if GTAS line #1000 is populated for the same TAS as of the end of the same reporting period.
WITH appropriation_a36_{0} AS
    (SELECT row_number,
        budget_authority_unobligat_fyb,
        tas,
        display_tas,
        submission_id
    FROM appropriation
    WHERE submission_id = {0})
SELECT
    approp.row_number,
    approp.budget_authority_unobligat_fyb,
    SUM(sf.amount) AS "expected_value_GTAS SF133 Line 1000",
    SUM(-sf.amount) AS "difference",
    approp.display_tas AS "uniqueid_TAS"
FROM appropriation_a36_{0} AS approp
    INNER JOIN sf_133 AS sf
        ON approp.tas = sf.tas
    INNER JOIN submission AS sub
        ON approp.submission_id = sub.submission_id
        AND sf.period = sub.reporting_fiscal_period
        AND sf.fiscal_year = sub.reporting_fiscal_year
WHERE sf.line = 1000
    AND approp.budget_authority_unobligat_fyb IS NULL
GROUP BY approp.row_number,
    approp.budget_authority_unobligat_fyb,
    approp.display_tas
HAVING SUM(sf.amount) <> 0;
