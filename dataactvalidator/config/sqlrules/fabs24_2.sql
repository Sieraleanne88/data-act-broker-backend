-- PrimaryPlaceOfPerformanceCountryCode must contain a valid three character GENC country code for aggregate or
-- non-aggregate records (RecordType = 1 or 2). U.S. Territories and Freely Associated States must be submitted with
-- country code = USA and their state/territory code; they cannot be submitted with their GENC country code.
SELECT
    row_number,
    record_type,
    place_of_perform_country_c,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM fabs
WHERE submission_id={0}
    AND record_type IN (1, 2)
    AND NOT EXISTS (
        SELECT 1
        FROM country_code AS cc
        WHERE UPPER(fabs.place_of_perform_country_c) = UPPER(cc.country_code)
            AND cc.territory_free_state IS FALSE
    )
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D';