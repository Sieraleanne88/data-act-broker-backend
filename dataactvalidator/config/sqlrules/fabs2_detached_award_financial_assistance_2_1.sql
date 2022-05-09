-- The combination of FAIN, AwardModificationAmendmentNumber, URI, CFDA_Number, and AwardingSubTierAgencyCode must be
-- unique from currently published ones unless the record is a correction or deletion, if
-- CorrectionDeleteIndicator = C or D.
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
    INNER JOIN published_fabs AS pf
        ON UPPER(dafa.afa_generated_unique) = UPPER(pf.afa_generated_unique)
        AND pf.is_active = TRUE
WHERE dafa.submission_id = {0}
    AND COALESCE(UPPER(dafa.correction_delete_indicatr), '') NOT IN ('C', 'D');
