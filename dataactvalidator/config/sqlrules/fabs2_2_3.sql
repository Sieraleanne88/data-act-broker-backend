-- The unique combination of FAIN, AwardModificationAmendmentNumber, URI, CFDA_Number, and AwardingSubTierAgencyCode
-- must exist as a currently published record when the record is a deletion (i.e., if CorrectionDeleteIndicator = D).
SELECT
    dafa.row_number,
    dafa.fain,
    dafa.award_modification_amendme,
    dafa.uri,
    dafa.awarding_sub_tier_agency_c,
    dafa.cfda_number,
    dafa.correction_delete_indicatr,
    dafa.afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM detached_award_financial_assistance AS dafa
WHERE dafa.submission_id = {0}
    AND COALESCE(UPPER(dafa.correction_delete_indicatr), '') = 'D'
    AND NOT EXISTS (
        SELECT 1
        FROM published_fabs AS pf
        WHERE UPPER(dafa.afa_generated_unique) = UPPER(pf.afa_generated_unique)
            AND pf.is_active = TRUE
    );
