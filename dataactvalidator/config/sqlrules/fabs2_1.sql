-- The combination of FAIN, AwardModificationAmendmentNumber, URI, CFDA_Number, and AwardingSubTierAgencyCode must be
-- unique within the submission file.
SELECT
    row_number,
    fain,
    award_modification_amendme,
    uri,
    awarding_sub_tier_agency_c,
    cfda_number,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM (
    SELECT dafa.row_number,
        dafa.fain,
        dafa.award_modification_amendme,
        dafa.uri,
        dafa.awarding_sub_tier_agency_c,
        dafa.cfda_number,
        dafa.afa_generated_unique,
        ROW_NUMBER() OVER (PARTITION BY
            UPPER(dafa.afa_generated_unique)
            ORDER BY dafa.row_number
        ) AS row
    FROM detached_award_financial_assistance AS dafa
    WHERE dafa.submission_id = {0}
    ) duplicates
WHERE duplicates.row > 1