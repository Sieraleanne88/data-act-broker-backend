-- NonFederalFundingAmount must be blank for loans (i.e., when AssistanceType = 07 or 08).
SELECT
    row_number,
    assistance_type,
    non_federal_funding_amount,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM detached_award_financial_assistance
WHERE submission_id = {0}
    AND (assistance_type = '07' OR assistance_type = '08')
    AND non_federal_funding_amount IS NOT NULL
    AND non_federal_funding_amount <> 0
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D';
