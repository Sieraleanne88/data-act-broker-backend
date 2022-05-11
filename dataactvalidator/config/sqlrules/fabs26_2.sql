-- FederalActionObligation is required for non-loans (i.e., when AssistanceType is not 07 or 08).
SELECT
    row_number,
    assistance_type,
    federal_action_obligation,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM detached_award_financial_assistance
WHERE submission_id = {0}
    AND assistance_type <> '07'
    AND assistance_type <> '08'
    AND federal_action_obligation IS NULL
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D';
