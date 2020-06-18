-- Unique FAIN or URI from file D2 should exist in file C, except for:
-- 1) Loans (AssistanceType = 07 or 08) with OriginalLoanSubsidyCost <= 0 in D2;
-- or 2) Non-Loans with FederalActionObligation = 0 in D2.
-- For non-aggregate and PII-redacted non-aggregate records, only the FAIN in D2 will be compared to C.
-- For aggregate records, only the URI in D2 will be compared to C.
-- Note that for File C, FAIN and URI cannot be provided on the same row.
WITH award_financial_assistance_c9_{0} AS
    (SELECT submission_id,
        row_number,
        federal_action_obligation,
        original_loan_subsidy_cost,
        fain,
        uri,
        assistance_type,
        record_type
    FROM award_financial_assistance
    WHERE submission_id = {0}),
award_financial_c9_{0} AS
    (SELECT submission_id,
        row_number,
        fain,
        uri
    FROM award_financial
    WHERE submission_id = {0}
        AND transaction_obligated_amou IS NOT NULL)
SELECT
    afa.row_number AS "source_row_number",
    afa.fain AS "source_value_fain",
    afa.uri AS "source_value_uri",
    afa.fain AS "uniqueid_FAIN",
    afa.uri AS "uniqueid_URI"
FROM award_financial_assistance_c9_{0} AS afa
WHERE ((afa.assistance_type NOT IN ('07', '08')
            AND COALESCE(afa.federal_action_obligation, 0) <> 0
        )
        OR (afa.assistance_type IN ('07', '08')
            AND COALESCE(CAST(afa.original_loan_subsidy_cost AS NUMERIC), 0) > 0
        )
    )
    AND ((afa.fain IS NOT NULL
            AND afa.record_type IN ('2', '3')
            AND NOT EXISTS (
                SELECT 1
                FROM award_financial_c9_{0} AS af
                WHERE UPPER(af.fain) = UPPER(afa.fain)
            )
        )
        OR (afa.uri IS NOT NULL
            AND afa.record_type = '1'
            AND NOT EXISTS (
                SELECT 1
                FROM award_financial_c9_{0} AS af
                WHERE UPPER(af.uri) = UPPER(afa.uri)

            )
        )
    );
