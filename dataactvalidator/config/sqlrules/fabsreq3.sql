-- RecordType is required for all submissions except delete records, but was not provided in this row.
SELECT
    row_number,
    record_type,
    correction_delete_indicatr,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM detached_award_financial_assistance
WHERE submission_id = {0}
    AND record_type IS NULL
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D';
