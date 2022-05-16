-- When provided, PeriodOfPerformanceCurrentEndDate must be a valid date between 19991001 and 20991231.
SELECT
    row_number,
    period_of_performance_curr,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM fabs
WHERE submission_id = {0}
    AND ((CASE WHEN is_date(COALESCE(period_of_performance_curr, '0'))
                THEN CAST(period_of_performance_curr AS DATE)
            END) < CAST('19991001' AS DATE)
        OR (CASE WHEN is_date(COALESCE(period_of_performance_curr, '0'))
                THEN CAST(period_of_performance_curr AS DATE)
            END) > CAST('20991231' AS DATE)
    )
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D';
