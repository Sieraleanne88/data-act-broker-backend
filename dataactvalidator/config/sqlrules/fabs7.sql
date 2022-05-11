-- URI is a required field for aggregate records (i.e., when RecordType = 1)
SELECT
    row_number,
    record_type,
    uri,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM detached_award_financial_assistance
WHERE submission_id = {0}
    AND record_type = 1
    AND (uri IS NULL
        OR uri = ''
    )
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D';
